from constents import supportedInstructions
import re

file=open("test1.s")
code=file.read().lower()
file.close()

code=re.sub(r"\s*#.*",'',code)#removing comments
code=re.sub(r"\s*,\s*",",",code)
code=re.sub(r"\s*(\n\s*)+","\n",code)#removing empty lines and those who are just set of spaces and the trilling extra spaces
code=re.sub(r"\s{2,}",' ',code)#removing extra spaces between words
instructionsText= re.search(r"_start\s*:\s([-\w\s,:()]+)\.?",code)
instructionsList=instructionsText.group().splitlines()
labels={}

for i, inst in enumerate(instructionsList):
	if inst.endswith(":") :
		labels[inst]=i+1
	else:
		if inst in supportedInstructions:
			tokens=re.split(r"(?:\s|,)+",inst)
			instructionsList[i]=tokens
