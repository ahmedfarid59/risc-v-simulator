from constents import regsNames

class registers(dict):
	def __init__(self):
		super().__init__( { key.upper() : 0 for key in regsNames.values() })

	def __setitem__(self, key, value):
		key = regsNames.get(key.upper(), key.upper())
		if key != 'X0' and key in self:
			value=int(value)&0xffffffff
			super().__setitem__(key, value)

	def __getitem__(self, key):
		key = regsNames.get(key.upper(), key.upper())
		return super().__getitem__(key)

	def get(self, key):
		key = regsNames.get(key.upper(), key.upper())
		return super().get(key)

	def __delitem__(self, key):
		pass

	def __str__(self):
		string = "-"*36+"\n"
		for key, value in self.items():
			string += f"{key} \t {value} \t {hex(value)} \t {bin(value)} \n"
		string+= "-"*36
		return string

