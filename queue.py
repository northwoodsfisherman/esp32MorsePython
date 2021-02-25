class Queue:
	def __init__(self):
		pass
		
		self.queue = []
	
	def add(self,s):
		self.queue.append(s)
		
	def dump(self):
		s = ''
		while len(self.queue) > 0:
			s = s + self.queue.pop(0)
		return(s)
	def remove(self):
		if len(self.queue) > 0:
			return(self.queue.pop(0))
		else:
			return('')
		
	
