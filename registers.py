from constents import regsNames

class registers(dict):
	def __init__(self):
		super().__init__( { key : 0 for key in regsNames.values() })

	def __setitem__(self, key, value):
		key = regsNames.get(key.lower(), key.lower())
		if key != 'x0' and key in self:
			value&=0xffffffff
			super().__setitem__(key, value)

	def __getitem__(self, key):
		key = regsNames.get(key.lower(), key.lower())
		return super().__getitem__(key)

	def get(self, key):
		key = regsNames.get(key.lower(), key.lower())
		return super().get(key)

	def __delitem__(self, key):
		pass

	def __str__(self):
		string = ""
		for key, value in self.items():
			string += key + "\t" + str(value) + "\n"
		return string

