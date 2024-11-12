from functions import *

instructionsFuncs=globals()
while pc < len(instructionsList):
	ins = instructionsList[pc]
	if ins[0] in supportedInstructions:
		function = instructionsFuncs[ins[0]]
		function(*ins[1:])
	elif ins[0] in holding:
		break
	print(" \t ".join(ins))
	print(regs)
	pc+=1
