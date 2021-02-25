 
import usocket,network,utime
import tt24
from cwSpeed import *
from random import seed,randint,getrandbits
from machine import reset


class TcpServer:
	def __init__(self,dataQueue,printQueue,params,speedControl,xmit):		

		self.dataQueue = dataQueue
		self.printQueue = printQueue
		self.speedControl = speedControl
		self.transmitter  = xmit

		self.myip = ''
		self.sock = object()
		self.con = object()
		self.addr = ()
		
		
		self.ssid = params.getp('ssid')
		self.wifiPassword = params.getp('wifiPassword')
		self.socketNo = params.getp('mySocket')
		self.presets = params.getp('presets')
		self.messages = params.getp('messages')
		self.remotePassword = params.getp('remotePassword')
		self.welcome = params.getp('welcome_msg')
		self.helpFile = """\r Help File\r\n\r\n \
)Hit (Shift)1,2, or 3 to send the corresponding canned message\r\n \
)ctrl+v to control the volume\r\n \
)ctrl+s to control the speed\r\n \
)ctrl+p to send random groups of CW for practice\r\n \
)ctrl+c to clear the transmit buffer area\r\n \
)ctrl+d to disconnect from ESP32\r\n \
)ctrl+r to reset the unit\r\n"""
		
		self.state= 0
		
		
		# defines for vt100 emulatore
		self.CLEAR_HOME = '\x1b[2J\x1b[H'  #clear entire screeen and set to home
		self.SET_KEYBOARD_SCROLL = '\x1b[7;35r'  #set scroll area
		self.CURSOR_KB_TOP = '\x1b[7;0H'	#move cursor to top  of scroll area
		self.CLEAR_CURSOR_DOWN = '\x1b[J'
		self.CURSOR_TO_STATUS_ROW = '\x1b[5;0f' #move cursor to status row 
		self.SAVE_CURSOR = '\x1b[s'
		self.RESTORE_CURSOR = '\x1b[u'
		self.CLEAR_LINE = '\x1b[K'
		
		
	def server(self):
		while(True):
			if self.state == 0:
				if self.getConnection():
					self.state  = 1
				else:
					return(False)
			elif self.state == 1:
				try:
					if self.getSocket():
						self.state = 2
				except:
					print('Socket Error')
					self.state = 0
			elif self.state == 2:
				if not self.listen():
					self.state = 1

	def getConnection(self):
		if self.ssid == '':
			return(False)
		wlan = network.WLAN(network.STA_IF)
		wlan.active(True)
		counter = 0
		if not wlan.isconnected():
			s = 'Connecting to: ' + self.ssid
			x = [2,50,tt24,s,False]
			self.printQueue.add(x)
			print(self.ssid)
			wlan.connect(self.ssid,self.wifiPassword)
			while not wlan.isconnected():
			
				print('.',end='')
				if counter > 20:
					x = [2,50,tt32,'WiFi Failed',False]
					self.printQueue.add(x)
					print(s)
					return(False)
				self.counter = counter+1
				utime.sleep(1)
		config = wlan.ifconfig()
		self.myip = config[0]
		s = 'Connected..My IP is: ' + self.myip
		x = [2,50,tt24,s,False]
		self.printQueue.add(x)
		print(s)		
		return(True)

	def getSocket(self):
		try:
			myaddr = usocket.getaddrinfo(self.myip,self.socketNo)[0][-1]
			self.sock = usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
			self.sock.setsockopt(usocket.SOL_SOCKET,usocket.SO_REUSEADDR, 1)
			self.sock.bind(myaddr)
			self.sock.listen(5)
			return(True)
		except Exception as e:
			print(e)
			s = 'Socket Error'
			print(s)
			x = [2,80,tt24,s,False]
			self.printQueue.add(x)
			return(False)

			
	def listen(self):
		
		while True:
			
			try:
				self.con,self.addr = self.sock.accept()
				#self.con = ussl.wrap_socket(self.con, server_side=True)
				s = 'Connection from: ' + str(self.addr[0])
				print(s)
				
				x = [2,80,tt24,s,False]
				self.printQueue.add(x)
				
				self.checkPassword()  #will  not return until there is a good password
				#password ok.. set up the screen
				self.sendResponse(self.CLEAR_HOME)  #clear screen
				
				self.sendResponse(self.welcome)
				self.sendResponse(self.SET_KEYBOARD_SCROLL)  #set scroll area
				self.sendResponse(self.CURSOR_KB_TOP)  #cursor to top of keyboard area
				self.writeStatus(s)   #info for status line
			except Exception as e:
				print(e)
				s = 'Connection Failed'
				x = [2,80,tt24,s,False]
				self.printQueue.add(x)
				print(s)
				self.sock.close()
				return(False)
			while True:
				try:
					asciiData = ''
					data,remoteAddress = self.con.recvfrom(100)
					if data == b'':
						self.con.close()
						s = 'Closing Connection'
						print(s)
						x = [2,100,tt24,s,False]
						self.printQueue.add(x)
						break;
					if data:
						
						self.processInput(data)
						
				except Exception as e:
					self.con.close()
					print(e)
					print('closing')
					break;
					
	def checkPassword(self):
		if self.remotePassword == '':
			return(True)
		
			
		while True:
			
			ascii = ''
			password = ''
			self.sendResponse(self.CLEAR_HOME)  #clear screen and set cursor to top of screen
			self.sendResponse('\r\nEnter Password:')
			while True:
				byteData = self.con.recv(1)
				if byteData == b'':
					return False #disconnected
				try:
					ascii = byteData.decode('ascii')
				except UnicodeError:
					password = ''
					continue
				if ascii == '\r':
					if password == self.remotePassword:
						return True
					else:
						self.sendResponse('\r\nLogin Failed\r\n')
						break  #start over again
				if self.isprintable(ascii):
					password = password + ascii
				
	def isprintable(self,ascii):
		if ascii < ' ':
			return False
		else:
			return True
				
		
	def processInput(self,byteData):
		#if data contains a special character, process it
		# there may be more than 1 character in byteData
		ascii = ''
		i = ''
		trigger = ''
		response = ''
		trigger = byteData	
		if trigger in self.presets: #is this a preset message?
			i = self.presets[trigger]
			tosend = self.messages[i]
			self.sendResponse( tosend + '\r\n')		
			for s in tosend:
				self.dataQueue.add(s)
			
			return
		elif trigger == b'\x03':  #ctl-c to clear the screen
			self.sendResponse(self.CURSOR_KB_TOP + self.CLEAR_CURSOR_DOWN)
		elif trigger == b'\x04':  #close the connection
			self.writeStatus('Connection Closed')
			utime.sleep(1)
			self.con.close()
		
		elif trigger == b'\x13': # of to set the speed?
			self.sendResponse(self.CURSOR_KB_TOP + self.CLEAR_CURSOR_DOWN)
			self.sendResponse('\r\nEnter Speed in WPM:')
			response = ''
			
			for i in range(0,4):
				byteData,remoteAddress = self.con.recvfrom(100)
				if byteData == b'':
					return  #disconnected
				try:
					ascii = byteData.decode('ascii')
				except UnicodeError:
					print('decoding error in speed')
					return
				if ascii[0] == '\r':
					self.speedControl.setWPM(int(response))
					tosend = '\r\nOK\r\n'
					self.sendResponse('\r\nOK\r\n')
					return
				response = response + ascii[0]
			return # too many characters	
			
		elif trigger == b'\x16': # of to set the speed?
			self.sendResponse(self.CURSOR_KB_TOP + self.CLEAR_CURSOR_DOWN)
			self.sendResponse('\r\nEnter Volume Level (0 to 255): ')
			response = ''
			
			for i in range(0,4):
				byteData,remoteAddress = self.con.recvfrom(50)
				if byteData == b'':
					return  #disconnected
				try:
					ascii = byteData.decode('ascii')
				except UnicodeError:
					print('decoding error in volume')
					return
				if ascii[0] == '\r':
					self.transmitter.setSideToneVolume(int(response))
					tosend = '\r\nOK\r\n'
					self.sendResponse('\r\nOK\r\n')
					return
				response = response + ascii[0]
			return # too many characters
		elif trigger == b'\x08':
			self.sendResponse(self.CURSOR_KB_TOP + self.CLEAR_CURSOR_DOWN)
			self.sendResponse(self.helpFile) 
		elif trigger == b'\x10':
			self.sendResponse(self.CURSOR_KB_TOP + self.CLEAR_CURSOR_DOWN)
			self.sendResponse('Prepare to Copy\r\n')
			self.dataQueue.add('vvvvv')
			for i in range(1,6):
				seed(getrandbits(6))
				for j in range(1,6):
					
					value = randint(48,90)
					ascii = chr(value)
					self.dataQueue.add(ascii)
					self.sendResponse(ascii)
				self.dataQueue.add(' ')
				self.sendResponse(' ')
			self.sendResponse('\r\n')
				
		elif trigger == b'\x12':
			self.sendResponse('\r\nResetting in 5 seconds\r\n')
			utime.sleep(5)
			reset()
			
		else:
			if byteData == b'\r\n':  
				self.con.sendall(byteData)
			try:
				ascii = byteData.decode('ascii')
			except UnicodeError:
				return
			self.dataQueue.add(ascii)
			
	def sendResponse(self,response):
		self.con.sendall(response.encode())
		
	def writeStatus(self,s):
		#remember the cursor position, move to status line, clear it, write new text s
		
		self.sendResponse(self.SAVE_CURSOR)
		self.sendResponse(self.CURSOR_TO_STATUS_ROW)
		self.sendResponse(self.CLEAR_LINE)
		self.sendResponse(s)  #write actual text
		self.sendResponse(self.RESTORE_CURSOR)
				

					
				
		
				
	
		
		
