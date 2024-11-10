from constents import supportedInstructions
import re

file=open("test1.s")#openning the file
code=file.read().lower()#getting the content of the file and converting it to lower case
file.close()#closing the file

code=re.sub(r"\s*#.*",'',code)#removing comments
code=re.sub(r"\s*,\s*",",",code)
code=re.sub(r"\s*(\n\s*)+","\n",code)#removing empty lines and those who are just set of spaces and the trilling extra spaces
code=re.sub(r"\s{2,}",' ',code)#removing extra spaces between words

#getting the instructions part of the code starting from the start label til the end of the file
instructionsText= re.search(r"_start\s*:\s([-\w\s,:()]+)\.?",code)
instructionsCode=instructionsText.group().splitlines()

labels={} #dictianary holds the labels and their indexes
instructions=[]

for i, inst in enumerate(instructionsCode):
	if inst.endswith(":") :
		labels[inst]=i+1
	else:
		if inst in supportedInstructions:
			tokens=re.split(r"(?:\s|,)+",inst)
			instructions.append(tokens)
