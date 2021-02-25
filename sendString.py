

from transmitter import *
from cwSpeed import *

import utime

class SendString:
	def __init__(self,xmitter,speed):
		self.key = xmitter  #object for the transmitter
		self.speed = speed   #object for the speed control
		
		self.queue = []
		self.state = 0
		self.mask = 0
		self.code = 0
		self.dotLength = 100
		self.dashLength = 300
		self.deadline = utime.ticks_ms()
		
		self.asciiToMorse = {
		'a':0x05, 
		'b':0x18, 
		'c':0x1a, 
		'd':0x0c, 
		'e':0x02, 
		'f':0x12, 
		'g':0x0e, 
		'h':0x10, 
		'i':0x04, 
		'j':0x17, 
		'k':0x0d,
		'l':0x14, 
		'm':0x07,
		'n':0x06, 
		'o':0x0f, 
		'p':0x16, 
		'q':0x1d, 
		'r':0x0a, 
		's':0x08, 
		't':0x03, 
		'u':0x09, 
		'v':0x11, 
		'w':0x0b, 
		'x':0x19,
		'y':0x1b, 
		'z':0x1c,  
#start of numbers
		'0':0x3f, 
		'1':0x2f, 
		'2':0x27, 
		'3':0x23, 
		'4':0x21, 
		'5':0x20, 
		'6':0x30, 
		'7':0x38, 
		'8':0x3c, 
		'9':0xe3, 
#punctuation
		'.':0x55,
		',':0x73,
		':':0x78,
		'?':0x4c,
	#	'\':0x5e,
		'-':0x6,
		'/':0x32,
		'(':0x6d,
		')':0x6d,
		'"':0x52,
		'@':0x5a,
		'=':0x31,
		' ':0x00
		}
		
	def codeString(self,s = ''):
		for c in s:
			try:
				c = c.lower()
				coded = self.asciiToMorse[c]
				self.queue.append(coded)
			except UnicodeError:
				continue
			except KeyError:
				continue
			except AttributeError:
				continue
			
		
	def sendCode(self):
		
		if self.state == 0:	#waiting for a char to arrive..do nothing
			self.dotLength = self.speed.getDotLength()
			self.dashLength = self.speed.getDashLength()
			if len(self.queue) > 0:
				#in this state...
				#take first char on the list. Find the highest set bit
				#this is the set of the coding. 
			
				self.code = self.queue.pop(0)
				
				#find left most set bit
				self.mask = 0x80
					#
				while self.mask & self.code == 0:
					if self.mask == 0:
						#got a space..no tones, just do interword time
						break;
					self.mask = self.mask >> 1	#keep looking for first set bit
				if self.mask == 0:
					self.deadline = utime.ticks_add(utime.ticks_ms(), 7 * self.dotLength)
					self.state = 4
				#at marker bit.. shift 1 more
				else:
					self.mask = self.mask >> 1  #now at right bit		
					self.state = 1
			else:
				return	#nothing to do
		elif self.state == 1: #determine if this element is a dash or dot
			if self.mask & self.code != 0:
				self.deadline = utime.ticks_add(utime.ticks_ms(),self.dashLength)
				self.state = 2
			else:
				self.state = 2
				self.deadline = utime.ticks_add(utime.ticks_ms(),self.dotLength)
			self.mask = self.mask >> 1  #get ready for next element(after waiting)
			self.key.transmit(True)		
		elif self.state == 2:
			#wait for or dash or dot to be done
			if utime.ticks_diff(self.deadline,utime.ticks_ms()) < 0:
				self.state = 3  #tone done
				self.key.transmit(False)
				#now wait for inter char time (ie..1 dotLength)
				self.deadline = utime.ticks_add(utime.ticks_ms(),self.dotLength)
		elif self.state == 3:
			#wait for inter character space to be done
			if utime.ticks_diff(self.deadline,utime.ticks_ms()) < 0:
				if self.mask == 0:
					#character is done... now add inter letter space
					self.deadline = utime.ticks_add(utime.ticks_ms(), self.dashLength)
					self.state = 4
				else:
					self.state = 1   #all with this element... process next element
		elif self.state == 4:
			if utime.ticks_diff(self.deadline,utime.ticks_ms()) < 0:
				#done with character.. go get another one
				self.state = 0
				
	
