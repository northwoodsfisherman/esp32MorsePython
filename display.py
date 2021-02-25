import tuneableParameters
from ili9341 import *
from machine import Pin, SPI
import tt14
import tt24
import tt32


class Display(ILI9341):
	def __init__(self,height=320,width=240,rotation=3,printQueue=object()):
		self.printQueue = printQueue
		
		self.spi = SPI(
			2,
			baudrate=40000000,
			miso=Pin(tuneableParameters.TFT_MISO_PIN),
			mosi=Pin(tuneableParameters.TFT_MOSI_PIN),
			sck=Pin(tuneableParameters.TFT_CLK_PIN))

		super().__init__(
			self.spi,
			Pin(tuneableParameters.TFT_CS_PIN),
			Pin(tuneableParameters.TFT_DC_PIN),
			Pin(tuneableParameters.TFT_RST_PIN),
			height,
			width,
			rotation)
		
		power = Pin(tuneableParameters.TFT_LED_PIN, Pin.OUT)
		power.value(1)
		
		self.erase()
		
		self.receivedText = ''
		
	def queuePrint(self,y):
		self.printQueue.add(y)
	
	def displayPrintQueue(self):
		while True:
			p = self.printQueue.remove()
			if p == '':
				return	
			if p[4] is False:	#no scroll
				self.set_pos(p[0],p[1])
				self.set_font(p[2])
				self.print(p[3])
			else:  #scroll
				self.receivedText = self.receivedText + p[3] #add on the one at the end
				self.receivedText = self.receivedText[-20:]  #just keep newest text
				self.set_pos(p[0],p[1])
				self.set_font(p[2])
				self.print(self.receivedText)
			
		
