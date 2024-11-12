import os
from constents import *
import re

#fileName=input("enter the risc-v file name")
#while not  os.path.exists(fileName):
	#print("file do not exist!")
		#fileName=input("enter the risc-v file name")

file=open("test1.s")#openning the file
code=file.read().lower()#getting the content of the file and converting it to lower case
file.close()#closing the file

code=re.sub(r"\s*#.*",'',code)#removing comments
code=re.sub(r"\s*,\s*",",",code)
code=re.sub(r"\s*(\n\s*)+","\n",code)#removing empty lines and those who are just set of spaces and the trilling extra spaces
code=re.sub(r"\s{2,}",' ',code)#removing extra spaces between words
code=code.upper()

textSection= re.search(r"\.TEXT\s*([-\w\s,:()]+)\.?",code).group().splitlines()
labels={} #dictianary holds the labels and their indexes
instructions=[]

for i, inst in enumerate(textSection):
	if inst.endswith(":") :
		labels[inst]=i
	else:
		if inst in supportedInstructions:
			tokens=re.split(r"(?:\s|,)+",inst)
			instructions.append(tokens)
		elif inst in holding:
			instructions.append(inst)

dataSection= re.search(r'\.DATA\s*([^\s]+(?:\s+[^\s]+)*)\s*(?=\n\s*\.TEXT)', code).group(1)
initialData=re.findall(r'(\w+)\s*:\s*\.(WORD|ASCII|ASCIZ|HALF|BYTE|DWORD)\s*([^\s]+)',dataSection)
vars={}
memory=bytearray(1048576)
pointer=0
for d in initialData:
	if d[1] =="WORD":
		value=d[2].split(',')
		if len(value)==1:
			memory[pointer:pointer+4]=int(d[2]).to_bytes(4,byteorder='big')
			pointer+=4
		else:
			for v in value:
				memory[pointer:pointer+4]=int(v).to_bytes(4,byteorder='big')
				pointer+=4
	elif d[1] =="HALF":
		memory[pointer:pointer+2]=int(d[2]).to_bytes(2,byteorder='big')
		pointer+=2
	elif d[1] == "BYTE":
		memory[pointer:pointer+1] = int(d[2]).to_bytes(1,byteorder='big')
		pointer+=1
	elif d[1] == "DWORD":
		memory[pointer:pointer+8]=int(d[2]).to_bytes(8,byteorder='big')
		pointer+=8
	elif d[1] == "ASCII":
		l=len(d[2])
		encoded=d[2].encode('utf-8')
		memory[pointer:pointer+l]=encoded
		pointer+=l
	elif d[1] == "ASCIZ":
		encoded=d[2][1:-1].encode('utf-8')+b'\0'
		l=len(encoded)
		memory[pointer:pointer+l]=encoded
		pointer+=l

