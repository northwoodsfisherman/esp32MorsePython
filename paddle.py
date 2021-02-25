from machine import Pin
import tuneableParameters

class Paddle:
	def __init__(self):
		self.dotPin = Pin(tuneableParameters.DOT_PIN,Pin.IN,Pin.PULL_UP)
		self.dashPin = Pin(tuneableParameters.DASH_PIN,Pin.IN,Pin.PULL_UP)
		
		
	def getPaddleState(self):
		# return: 0  (both pressed)
		# return: 1  (dash pressed, dot not)
		#return 2 (dot pressed, dash not)
		#return 3 (neither pressed)
		if self.dotPin.value() == 0: 
			if self.dashPin.value() == 0:
				return(True,True)  #both pressed
			else:
				return(True,False) #dot pressed, dash not pressed
		else: 
			if self.dashPin.value() == 0:
				return(False,True) #dash pressed, dot not pressed
			else:
				return(False,False)  #neither pressed
		

	
