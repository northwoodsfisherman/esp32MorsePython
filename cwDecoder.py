from ElementsToCharsConverter import *

#from timer import Timer
from math import sin,cos,sqrt
from machine import ADC,Pin
import utime
LOW = 0
HIGH = 1

#should freq  be 558?
class CWdecoder:
	
	def __init__(self,target_freq,adcPin,outputQueue):
		
		self.toChars = ElementsToCharsConverter(outputQueue)
		
		self.target_freq = target_freq
		self.adc = ADC(Pin(adcPin))
		self.magnitute = 0.0
		self.magnitudelimit = 100
		self.magnitudelimit_low = 100
		self.realstate = LOW
		self.realstatebefore = LOW
		self.filteredstate = LOW
		self.filteredstatebefore = LOW
		# The sampling frequency ... add more here
		
		self.coeff = 0.0
		self.Q1 = 0.0
		self.Q2 = 0.0
		self.sine = 0.0
		self.cosine = 0.0
		#self.sampling_freq = 45000.0
		self.sampling_freq = 8928.0
		self.n = 48 #was 128
		self.testData = [0] * self.n 

		#self.testData(self.n)
		self.bw = 0.0
		
		# Noise blanker
		self.nbtime = 6
		self.starttimehigh = 0
		self.highduration = 0
		self.lasthighduration = 0
		self.hightimesavg = 0
		self.lowtimesavg = 0
		self.starttimelow = 0
		#self.starttimelow = Timer()
		self.lowduration = 0
		#self.lowduration = Timer()
		self.laststarttime = 0
		#self.laststarttime = Timer()
		#self.CodeBuffer[14] = []
		#self.DisplayLine[15] = []   #always one more
		self.CodeBuffer = []
		self.DisplayLine = []
		self.stop = 0  #LOW ?
		self.wpm = 0
		
		#set up display
		self.bw = self.sampling_freq / self.n
		self.k = (0.5 + ((self.n * self.target_freq) / self.sampling_freq ))
		self.omega = (6.28 * self.k)/self.n
		self.sine = sin(self.omega)
		self.cosine = cos(self.omega)
		self.coeff = 2.0 * self.cosine
	#	for i in DisplayLine:
	#		DisplayLine[i] = ''
		
		
		
	def cwDecoder(self):
		Q0 = 0.0
		#take a sample
		for i in range(0,self.n - 1):
			self.testData[i] = self.adc.read()
		for i in range(0,self.n - 1):
			self.Q0 = self.coeff * self.Q1 - self.Q2 + self.testData[i]
			self.Q2 = self.Q1
			self.Q1 = self.Q0
			
		self.magnitudeSquared = (self.Q1 * self.Q1) + (self.Q2* self.Q2) - self.Q1 * self.Q2 * self.coeff
		
		self.magnitude = sqrt(self.magnitudeSquared)
		
		self.Q1 = 0
		self.Q2 = 0
		
		if self.magnitude > self.magnitudelimit_low:
			self.magnitudelimit = (self.magnitudelimit+((self.magnitude - self.magnitudelimit) /6))
		if self.magnitudelimit < self.magnitudelimit_low:
			self.magnitudelimit = self.magnitudelimit_low
		if self.magnitude > self.magnitudelimit * 0.6:
			self.realstate = HIGH
		else:
			self.realstate = LOW
		# Clean up with a noise blanker
		
		if self.realstate != self.realstatebefore:
			self.laststarttime = utime.ticks_ms()
			
		if  utime.ticks_diff( utime.ticks_ms(), self.laststarttime) > self.nbtime:
			if self.realstate != self.filteredstate:
				self.filteredstate = self.realstate
				
		if self.filteredstate != self.filteredstatebefore:
			if self.filteredstate == HIGH:
				self.starttimehigh = utime.ticks_ms()
				self.lowduration = utime.ticks_diff(utime.ticks_ms(),self.starttimelow)
				
			if self.filteredstate == LOW:
				self.starttimelow = utime.ticks_ms() #records current time
				self.highduration = utime.ticks_diff(utime.ticks_ms(), self.starttimehigh )
				if ( self.highduration <  (2 * self.hightimesavg) ) or self.hightimesavg  == 0  :
					self.hightimesavg = (self.highduration + self.hightimesavg+self.hightimesavg ) / 3
				if self.highduration > (5 * self.hightimesavg):
					self.hightimesavg = self.highduration + self.hightimesavg
				
		#check baud rate based on dit or dah duration either 1,3, or 7 pauses
		
		if self.filteredstate != self.filteredstatebefore:
			self.stop = LOW
			if self.filteredstate == LOW:
				if self.highduration < (self.highttimesavg * 2) and self.highduration > (self.hightimesavg*0.6):
					print('.')
					self.toChars.elementsToChars('.')
				if (self.highduration > (self.hightimesavg * 2) ** self.highduration < (self.hightimesavg * 6)):
					print('-')
					self.toChars.elementsToChars('-')
					self.wpm = (wpm + (1200 / (( self.highduration)/ 3)))/ 2
					
		if  self.filteredstate == HIGH: # we did end on a low
			lacktime = 1.0
			if self.wpm > 25:
				lacktime = 1.0
			if self.wpm > 30:
				lacktime = 1.2
			if self.wpm > 35:
				lacktime = 1.5
			if self.lowduration > (self.hightimesavg * ( 2 * lacktime)) and self.lowduration < self.hightimesavg * ( 5 * lacktime):
				print('*')  #letter space.. start decoding again
				self.toChars.elementsToChars('*')
			if self.lowduration >= self.hightimesavg * ( 5 * lacktime):
				print(' ')  #word space
				self.toChars.elementsToChars(' ')
		if utime.ticks_diff(utime.ticks_ms(),self.starttimelow) > (self.highduration * 6) and self.stop == LOW:
			print(' ')
			self.stop = HIGH
		
		#clean up
		self.realstatebefore = self.realstate
		self.lasthighduration = self.highduration
			

		
			
			
				
		
			
			
		
		
		
		
		
		
		
