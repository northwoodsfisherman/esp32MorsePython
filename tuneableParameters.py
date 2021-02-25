from micropython import const
from machine import SPI,Pin
import uos,sdcard,ujson

#I/O Pins

TFT_LED_PIN = const(32)
TFT_DC_PIN = const(27)
TFT_CS_PIN = const(14)
TFT_MOSI_PIN = const(23)
TFT_CLK_PIN = const(18)
TFT_RST_PIN = const(33)
TFT_MISO_PIN = const(19)

SD_MOSI_PIN = const(23)
SD_MISO_PIN = const(19)
SD_CLK_PIN = const(18)
SD_CS_PIN = const(4)  #double use with M2?

TRANSMITTER_PIN = const(0)
SIDETONE_PIN = const(26)  #in analog mode
DOT_PIN = const(15)
DASH_PIN = const(2)
POT_PIN = const(34)
M1_PIN = const(4)
M2_PIN = const(13)

class TuneableParameters:
	def __init__(self):
		pass
		
		self.parameters = {
		'ssid':'DorrieNet',
		'wifiPassword':'ganshill1',
		'remotePassword':'1234',
		'mySocket':6000,
		'defaultSpeed':10,
		'presets':{b'!':0,b'@':1,b'#':2},
		'welcome_msg':'Welcome to the WB8WGA Remote CW Terminal\r\nHit ctrl+h for help\r\n',
		'messages':['cq fd cq fd de wb8wga wb8wga k',
		'bk de wb8wga report bk',
		'parisparisparisparis']
		}
		
	#	self.initSDC()

	def getp(self,s):
		return(self.parameters[s])
		
	def getm(self,i):
		messages = self.parameters['messages']
		return(messages[i])
		
	def initSDC(self):
		
		spi = SPI(1, baudrate=10000,sck=Pin(SD_CLK_PIN), mosi=Pin(SD_MOSI_PIN),miso=Pin(SD_MISO_PIN) )
		spi.init()
		
		try:
			sd = sdcard.SDCard(spi, Pin(SD_CS_PIN) )  # Compatible with PCB
			#check if any card exists
		
			vfs = uos.VfsFat(sd)
			uos.mount(vfs, "/fc")
			print("Filesystem check")
			print(uos.listdir("/fc"))
			uos.mount(sd, "/sd")
		except:
			print('SD card not detected')
			return
		#now see if parameters file is on the SD card
		try:		
			f = open('/sd/parameters.json','r')
			self.parameters = ujson.loads(f.read())   #read in the new parameters
			print('Reading params from the SD card')
			print(self.parameters)
		
		except:
			#sd card  plugged in but no paremeters file.. init card to current parameters
			print('Writing out defaults to disk')
			f = open('/sd/parameters.json','w')
			f.write(ujson.dumps(self.parameters))
		
		try:
			f.close()
			uos.umount(vfs)
			
		except:
			pass
		spi.deinit()
		del(spi)
		return
		
		
		
