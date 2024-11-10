from constents import regsNames

class regs:
	registersList = [0]*32
	@property
	def registersList(self):
		return self.registersList

	def preview(self):
		for i,name in enumerate(regsNames.keys()):
			print(name,self.registersList[i])
	
	def set(self,index,value):
		if index != 0:
			self.registersList[index]=value


