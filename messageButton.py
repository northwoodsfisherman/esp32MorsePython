import utime
from machine import Pin

class MessageButton:
	def __init__(self,pinNo,messageNumber,queue,params):
		self.pin = Pin(pinNo,Pin.IN,Pin.PULL_UP)
		self.queue = queue
		self.ticks = utime.ticks_ms()
		self.state = 0
		self.messages = params.getp('messages')
		self.message = self.messages[messageNumber]
		
	def insertPresetMessage(self):
		if self.state == 0:
			if self.pin.value() == 0:
				self.ticks = utime.ticks_add(utime.ticks_ms(),30)
				self.state = 1
				
		elif self.state == 1:
			if self.ticks - utime.ticks_ms() < 0:
				if self.pin.value() == 1:
					self.state = 0
					return
				self.queue.add(self.message)
				self.ticks = utime.ticks_add(utime.ticks_ms(),3000)
				self.state = 2
		elif self.state == 2:
			if self.ticks - utime.ticks_ms() < 0:
				self.state = 0
			
			
				
				
		
