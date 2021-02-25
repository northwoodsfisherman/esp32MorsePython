

from tuneableParameters import *
from tcpServer import *
from display import *
from cwDecoder import *
from messageButton import *
from iambic import *
from sendString import *
from paddle import *
from cwSpeed import *
from transmitter import *
import _thread
from queue import *

dataQueue = Queue()
pQueue = Queue()

display = Display(height=320,width=240,rotation=3,printQueue=pQueue)

#get the transmitter object
xmit = Transmitter() #get the transmitter object

display = Display(height=320,width=240,rotation=3,printQueue=pQueue)

#get a copy of all the tuneable parameters
params = TuneableParameters()

#get the Paddle object
paddle = Paddle()

#get the object to control speed
speedControl = cwSpeed(params)

#open the server for the remote terminal
remoteTerminal = TcpServer(dataQueue,pQueue,params,speedControl,xmit)

#open the decoder for reading cw
decoder = CWdecoder(496.0,34,pQueue)


#open the object to code and send strings
ss = SendString(xmit,speedControl)



keyer = Iambic(xmit,paddle,speedControl)

b1 = MessageButton(tuneableParameters.M1_PIN,2,dataQueue,params)
b2 = MessageButton(tuneableParameters.M2_PIN,1,dataQueue,params)


x = [2,5,tt32,'WB8WGA Keyer',False]
pQueue.add(x)


t = _thread.start_new_thread(remoteTerminal.server,())



while True:	
	conv = ElementsToCharsConverter(pQueue)
#	b1.insertPresetMessage()
#	b2.insertPresetMessage()
#	decoder.cwDecoder()
#	keyer.iambic()
	s = dataQueue.remove()
	
	if s != '':
		ss.codeString(s)
	ss.sendCode()
	display.displayPrintQueue()


