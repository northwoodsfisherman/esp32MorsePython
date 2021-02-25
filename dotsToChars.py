

class ElementsToCharsConverter:
	def __init__ (self,outputQueue):
		self.outputQueue = outputQueue
		self.dash = 0
		self.dot = 0
		
		self.translate = ['','E','T','I','A','N','M','S','U','R','W','D','K','G','O','H','V','F','-','L','-','P','J','B','X','C',\
		'Y','Z','Q','-','-','5','4','-','3','-','-','-','2','-','-','-','-','-','-','-','1','6','-','/','-',\
		'-','-','-','-','7','-','-','-','8','-','9','0','-','-','-','-','-','-','-','-','-','-','-','-','?',\
		'-','-','-','-','-','-','-','-','.','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-' ]
		
	def elementsToChars(self,element):
		if element == ' ' or element == '*':
			index = self.dash * 2 + self.dot
			if index < len(self.translate):
				#if too many characters.. don't attempt to print
				self.outputQueue(self.translate[index])
			self.dash = 0
			self.dot = 0
			return
		elif element == '.':
			self.dot = 2 * self.dot + 1
			self.dash = 2 * self.dash
		elif element == '-':
			self.dash = 2 * self.dash + 1
			self.dot = self.dot * 2
		else:
			#bad input, just return	
			return		
	
	#output to a queue... do something else if you want		
	def outputChar(self,c):
		self.outputQueue.add(c)
			
	
	
