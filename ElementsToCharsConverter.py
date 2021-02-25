import tt24

class ElementsToCharsConverter:
	def __init__ (self,outputQueue):
		self.outputQueue = outputQueue
		self.dash = 0
		self.dot = 0
		
		self.translate = ['','E','T','I','A','N','M','S','U','R','W','D','K','G','O','H','V','F','-','L','-','P','J','B','X','C',\
		'Y','Z','Q','-','-','5','4','-','3','-','-','-','2','-','-','-','-','-','-','-','1','6','-','/','-',\
		'-','-','-','-','7','-','-','-','8','-','9','0','-','-','-','-','-','-','-','-','-','-','-','-','?',\
		'-','-','-','-','-','-','-','-','.','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-' ]
		
	def elementsToChars(self,elements):
		for element in elements:
			index = self.dash * 2 + self.dot
			if index >= len(self.translate):
				#clearly not a valid character.. reset and start over
				self.dash = 0
				self.dot = 0
				continue
			if element == ' ' or element == '*':
				self.outputChar(self.translate[index])
				if element == ' ':
					self.outputChar(' ')  #insert a space between words
				self.dash = 0
				self.dot = 0
				continue
			elif element == '.':
				self.dot = 2 * self.dot + 1
				self.dash = 2 * self.dash
			elif element == '-':
				self.dash = 2 * self.dash + 1
				self.dot = self.dot * 2
			else:
				#bad input, just return	
				continue		
	
	#output to a queue... do something else if you want		
	def outputChar(self,c):
		x = [2,180,tt24,c,True]
		#remove this later
		print(c,end='')
		self.outputQueue.add(x)
			
	
	
