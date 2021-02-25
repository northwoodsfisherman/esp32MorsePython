from machine import ADC,Pin
import  tuneableParameters 

class cwSpeed:
	def __init__(self,params):
		self.params = params
		self.pot = ADC(Pin(tuneableParameters.POT_PIN ) )
		self.pot.atten(ADC.ATTN_11DB)
		self.pot.width(ADC.WIDTH_9BIT)
		self.speedWPM = self.params.getp('defaultSpeed')
		self.lengthofDot = int(1200/self.speedWPM)
		self.lengthofDash= self.lengthofDot * 3

	def readPot(self):  #from potentiometer
		self.speedWPM = self.pot.read() *(20/1023)+.5
		self.lengthofDot = int(1200/self.speedWPM)
		self.lengthofDash = self.lengthofDot * 3
		return(self.speedWPM)
		 
	def setWPM(self,wpm):  #from remote terminal
		self.lengthofDot = int(1200/wpm)
		self.lengthofDash = self.lengthofDot * 3
		self.speedWPM = wpm
	
	def getWPM(self):
		return(self.speedWPM)
		
		
	def getDashLength(self):
		return(self.lengthofDash)
		
	def getDotLength(self):
		return(self.lengthofDot)
	



