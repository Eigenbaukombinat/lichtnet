#coding:utf8
import socket
import struct
import time 

class ArtNet(object):
	def __init__(self,adress):
		self.SOCK = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.NODE_IP="10.110.115.10" # ip -- ArtnetNode =====>>>> hier ändern
		self.NODE_PORT=0x1936         # ArtNet Port
		self.ADRESS=adress

	def close(self):
		self.SOCK.close()
		
	def send_data(self, data):
		content = []
		# Name, 7byte + 0x00
		content.append("Art-Net" + "\x00")
		# OpCode ArtDMX -> 0x5000, Low Byte first
		content.append(struct.pack('<H', 0x5000))
		# Protocol Version 16, High Byte first
		content.append(struct.pack('>H', 16))
		# Order -> nope -> 0x00
		content.append("\x00")
		# Eternity Port
		content.append(chr(0))
		# Address
		net, subnet, universe = self.ADRESS
		content.append(struct.pack('<H', net << 8 | subnet << 4 | universe))
		# Length of DMX Data, High Byte First
		content.append(struct.pack('>H', len(data)))
		# DMX Data
		content += [chr(i) for i in data]
		# stitch together
		content = "" .join (content)
		self.SOCK.sendto(bytes(content), (self.NODE_IP, self.NODE_PORT))
	
# Test
r = [255,0,0,255]
g = [0,255,0,255]
b = [0,0,255,255]
s = [255,255,255,255,200,0]

univers=0
address = [0, 0, univers]
artnet=ArtNet(address)
artnet.send_data(r)
time.sleep(0.1)
artnet.send_data(g)
time.sleep(0.1)
artnet.send_data(b)
time.sleep(0.1)
artnet.send_data(r)
time.sleep(0.1)
artnet.send_data(g)
time.sleep(0.1)
artnet.send_data(b)
time.sleep(0.1)
artnet.send_data(s)
time.sleep(2.1)
artnet.send_data([0,0,0,0,0,0])
artnet.close()
