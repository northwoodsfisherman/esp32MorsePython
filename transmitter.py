from machine import Pin, DAC
import tuneableParameters 

class Transmitter:
	def __init__(self):
		self.xmitPin = Pin(tuneableParameters.TRANSMITTER_PIN,Pin.OUT,value=0)
		self.sideTone = DAC(Pin(tuneableParameters.SIDETONE_PIN))
		self.volume = 75  #255 is loudest
		
	def get_information(self):
		print('''
		Function: Keys the transmitter and turns on Sidetone
		based on TRANSMITTER_PIN and SIDETONE_PIN 
		Usage: x = Transmitter()
		x = Transmitter(),x.transmit(TRUE/FALSE), 
		x.setSideToneVolume(0 to 255) 255 is loudest''')
		
	def transmit(self,state):
		if state is True:
			self.xmitPin.value(1)
			self.sideTone.write(self.volume)
		else:
			self.xmitPin.value(0)
			self.sideTone.write(0)
	
	def setSideToneVolume(self,dacValue):
		self.volume = dacValue
	
