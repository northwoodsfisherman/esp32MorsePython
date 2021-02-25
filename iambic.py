from paddle import *
from transmitter import *
import utime

class Iambic:
	def __init__(self,xmit,paddle,speed):
		self.currentState = 0
		self.lastState = 0
		self.nextState = 0
		self.deadline = utime.ticks_ms()
		
		self.key = xmit  #objects for xmit,paddle, and speed
		self.paddle = paddle
		self.speed = speed
		
	def iambic(self):
				
		dot,dash = self.paddle.getPaddleState()
	
		if self.currentState == 0:  #idle state
			if dot and not dash: # Only Dot Paddle
				self.lastState = 0
				self.currentState = 1
				self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDotLength())
			elif dash and not dot: #dash and not dot
				self.lastState = 0
				self.currentState = 2
				self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDashLength())
			elif dash and dot and self.nextState == 0: #both dot and dash
				self.lastState = 0
				self.currentState = 1
				self.nextState = 2
				self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDashLength())
		#	self.key.transmitter(False)			
		
		elif self.currentState == 1: #dot
			if dash and dot: #dash and dot
				self.nextState = 2
			if utime.ticks_diff(self.deadline, utime.ticks_ms()) < 0 :
				self.lastState = 1
				self.currentState = 3
				self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDotLength())	
			self.key.transmitter(True)
		
		elif self.currentState == 2: #dash
		
			if dot and self.nextState == 0:
				self.nextState = 1
			if utime.ticks_diff(self.deadline, utime.ticks_ms()) < 0 :
				self.lastState = 2
				self.currentState = 3
				self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDotLength())
			self.key.transmitter(True)
		
		elif self.currentState == 3: #delay state
		
			if utime.ticks_diff(self.deadline, utime.ticks_ms()) < 0 :
				self.currentState = self.nextState
				if self.currentState == 1:
					self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDotLength())
				elif self.currentState == 2:
					self.deadline = utime.ticks_add(utime.ticks_ms(), self.speed.getDashLength())
				self.lastState = 3
				self.nextState = 0
			if dash and self.lastState == 1 and self.nextState == IDLE:
				self.nextState = 2
			elif dot and self.lastState == 2 and self.nextState == IDLE:
				self.nextState = 0
			self.key.transmitter(False)
		
		

