import artnet


class Channel(object):
    """Describes a channel"""

    def __init__(self, channel_id, description='Generic Channel'):
        self._description = description
        self.set_channel_id(channel_id)
        self.value = 0x00
        self.old_value = 0x00

    def set_channel_id(self, channel_id):
        self.channel_id = channel_id
        self.description = '{} (#{})'.format(self._description, channel_id)

    def blackout(self):
        self.value = 0x00


class Fixture(object):
    """Base class for an artnet fixture."""

    def __init__(self):
        self.num_channels = 0
        self.address = '255.255.255.255'
        self.channels = {}
        
    def add_channel(self, name, descr):
        self.channels[name] = Channel(name, descr)
        self.num_channels = len(self.channels.keys())

    def set_channel(self, name, value):
        channel = self.channels[name]
        channel.value = value

    def blackout(self):
        for channel in self.channels.values():
            channel.blackout()

    def set_base_channel(self, base_channel):
        for name, channel in  self.channels.items():
            channel.set_channel_id(channel.channel_id + base_channel)


class SingleLedFixture(Fixture):
    def __init__(self):
        self.num_channels = 1
        self.address = '255.255.255.255'
        self.channels = {'p': Channel(0, 'Value')}


class RGBFixture(Fixture):

    def __init__(self):
        self.num_channels = 4
        self.address = '255.255.255.255'
        self.channels = {'r': Channel(0, 'Red'),
                    'g': Channel(1, 'Green'),
                    'b': Channel(2, 'Blue'),
                    'm': Channel(3, 'Main'),}

    def set_color(self, r, g, b):
        self.set_channel('r', r)
        self.set_channel('g', g)
        self.set_channel('b', b)
    
    def set_main_brightness(self, brightness):
        self.set_channel('m', brightness)




class Universe(object):
    address = '255.255.255.255'
    data = 512*[0]
    fixture_channels = 512*[None]

    def __init__(self, artnet):
        self.address = '255.255.255.255'
        self.data = 512*[0]
        self.fixture_channels = 512*[None]
        self.artnet = artnet

    def register_fixture_channels(self, fix):
        fix.universe = self
        for name, channel in fix.channels.items():
            self.fixture_channels[channel.channel_id] = channel

    def update_data(self):
        for ch in self.fixture_channels:
            if ch is None:
                continue
            self.data[ch.channel_id] = ch.value
        self.send()

    def blackout(self):
        for ch in self.fixture_channels:
            if ch is not None:
                ch.blackout()
        self.send()
        
    def send(self):
        data = self.artnet.encode_channels(*zip(range(len(self.data)), self.data))
        self.artnet.sendArtDMX(self.address, data)

FIXTURES = {'rgb': RGBFixture, 'single': SingleLedFixture}

class Controller(object):
    universes = {}
    fixtures = {}

    def __init__(self):
        self.universes = {}
        self.fixtures = {}
        self.artnet = artnet.ArtNet()

    def add_fixture(self, name, type_, base_channel, address):
        fix = FIXTURES[type_]()
        fix.set_base_channel(base_channel)
        fix.address = address
        if not self.universes.has_key(address):
            universe = Universe(self.artnet)
            universe.address = address
            self.universes[address] = universe
       
        self.universes[address].register_fixture_channels(fix)
        self.fixtures[name] = fix

    def get_fixture(self, name):
        return self.fixtures[name]

    def send_update(self, fixture_names=None):
        if fixture_names is None:
            universes = set(self.universes.values())
        else:
            universes = set()
            for name in fixture_names:
                fix = self.fixtures[name]
                universes.add(self.universes[fix.address])
            
        for universe in universes:
            universe.update_data()


