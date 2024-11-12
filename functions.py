from parse import *
from registers import registers

regs = registers()

pc=0

def ADD(rd, rs1, rs2):
	regs[rd] = regs[rs1] + regs[rs2]

def SUB(rd, rs1, rs2):
	regs[rd] = regs[rs1] - regs[rs2]

def ADDI(rd, rs1, imm):
	regs[rd] = regs[rs1] + (imm & 0xfff)

def AND(rd, rs1, rs2):
	regs[rd] = regs[rs1] & regs[rs2]

def ANDI(rd, rs1, imm):
	regs[rd] = regs[rs1] & (imm &0xfff)

def OR(rd, rs1, rs2):
	regs[rd] = regs[rs1] | regs[rs2]

def ORI(rd, rs1, imm):
	regs[rd] = regs[rs1] | (imm&0xfff)

def XOR(rd ,rs1 ,rs2):
	regs[rd] = regs[rs1] ^ regs[rs2]

def XORI(rd, rs1, imm):
	regs[rd] = regs[rs1] ^ (imm&0xfff)

def SLLI(rd, rs1, imm):
	regs[rd] = regs[rs1] << (imm&0x1f)

def SRLI(rd, rs1, imm):
	regs[rd] = regs[rs1] >> (imm&0x1f)

def SLL(rd, rs1, rs2):
	regs[rd] = regs[rs1] << (regs[rs2] & 0x1F)

def SRL(rd, rs1, rs2):
	regs[rd] = ( regs[rs1] & 0xFFFFFFFF) >> (regs[rs2] & 0x1F)

def SRA(rd, rs1, rs2):
	regs[rd] = (regs[rs1] >> ((regs[rs2] % 32)+1))&(1<<31)

def SRAI(rd, rs1, imm):
	regs[rd] =(( regs[rs1]&0x7fffffff) >> (imm&0x1f))&0x80000000

def SLT(rd, rs1, rs2):
	regs[rd] = int(regs[rs1] < regs[rs2])

def SLTU(rd, rs1, rs2):
	regs[rd] = int(regs[rs1] < regs[rs2])

def SLTI(rd, rs1, imm):
	regs[rd] = int(regs[rs1] < (imm & 0xfff))

def SLTIU(rd, rs1, imm):
	regs[rd] = int((regs[rs1] & 0xFFFFFFFF) < (imm & 0xFFFFFFFF))

def BEQ(rs1, rs2, label):
	if regs[rs1] == regs[rs2]:
		pc=labels[label]

def BNE(rs1, rs2, label):
	if regs[rs1] != regs[rs2]:
		pc[label]

def BLT(rs1, rs2, label):
	if regs[rs1] < regs[rs2]:
		pc=labels[label]

def BGE(rs1, rs2, label):
	if regs[rs1] >= regs[rs2]:
		pc=labels[label]

def BLTU(rs1, rs2, label):
	if regs[rs1]  < regs[rs2] :
		pc=labels[label]

def BGEU(rs1, rs2, label):
	if regs[rs1] >= regs[rs2]:
		pc=labels[label]

# Load Instructions
def LB(rd, offset, rs1):
	addr = regs[rs1] + offset
	regs[rd] = int.from_bytes(memory[addr],byteorder='big',signed=True)

def LH(rd, offset, rs1):
	addr = regs[rs1] + offset
	regs[rd] = int.from_bytes(memory[addr:addr+2],byteorder='big',signed=True)

def LW(rd, offset, rs1):
	addr = regs[rs1] + offset
	regs[rd] = int.from_bytes(memory[addr:addr+4] , byteorder='big',signed=True)

def LBU(rd, offset, rs1):
	addr = regs[rs1] + offset
	regs[rd] = int.from_bytes(memory[addr], byteorder='big')

def LHU(rd, offset, rs1):
	addr = regs[rs1] +offset
	regs[rd] = int.from_bytes(memory[addr:addr+2], byteorder='big')

def AUIPC(rd, imm):
	regs[rd] = imm << 12 + rd

def LUI(rd, imm):
	regs[rd] = imm << 12

# Store Instructions
def SB(rs2, offset, rs1):
	addr = regs[rs1] + offset
	memory[addr] = (regs[rs2] & 0xff).to_bytes(1,byteorder='big')

def SH(rs2, offset, rs1):
	addr = regs[rs1] +offset
	memory[addr:addr+2] = (regs[rs2] & 0xffff).to_bytes(2,byteorder='big')

def SW(rs2, offset, rs1):
	addr = regs[rs1] +offset
	memory[addr:addr+4] = (regs[rs2] & 0xffffffff).to_bytes(4,byteorder='big')

#jump instructions
def JAL(rd, label):
	regs[rd] = pc
	pc=labels[label]

def JALR(rd, offset, rs1):
	regs[rd] =pc
	pc=regs[rs1] + offset

def MUL(rd, rs1, rs2):
	regs[rd] = regs[rs1] * regs[rs2]

def DIV(rd, rs1, rs2):
	regs[rd] = regs[rs1] // regs[rs2] if regs[rs2] != 0 else 0

def REM(rd, rs1, rs2):
	regs[rd] = regs[rs1] % regs[rs2] if regs[rs2] != 0 else 0

def MV(rd ,rs):
	regs[rd] = regs[rs]

def NOT(rd ,rs):
	regs[rd] = ~regs[rs]

def NEG(rd ,rs):
	regs[rd] = regs[rs] *-1

def LI(rd ,imm):
	regs[rd] = imm

def J(label):
	pc=labels[label]

def RET():
	pc=regs['x1']
