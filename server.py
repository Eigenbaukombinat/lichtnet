import logging
from flask import Flask, render_template
import dmxmodel


log = logging.getLogger('DMXWeb')


controller = dmxmodel.Controller()

controller.add_fixture('RGB1', 'rgb', 0, '10.110.115.10')
controller.add_fixture('RGB2', 'rgb', 4, '10.110.115.10')
controller.add_fixture('RGB3', 'rgb', 8, '10.110.115.10')

fixtures = {'r1': controller.get_fixture('RGB1'),
    'r2': controller.get_fixture('RGB2'),
    'r3': controller.get_fixture('RGB3')}

app = Flask(__name__)

@app.route('/')
def mainpage():
    return render_template('index.html')

def hex_to_int(h):
    return (int(h[0:2], 16),
        int(h[2:4], 16),
        int(h[4:6], 16))

@app.route('/color/<fixture>/<color>/<brightness>')
def color(fixture, color, brightness):
    fix = fixtures[fixture]
    fix.set_color(*hex_to_int(color))
    fix.set_main_brightness(int(brightness))
    controller.send_update()
    return 'OK'

