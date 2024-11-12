from parse import labels,instructions

registers = {i: 0 for i in range(32)}
memory = {}

def signage(value, bits):
	if value & (1 << (bits - 1)):
		return value | ~((1 << bits) - 1)
	return value

# Arithmetic and Logical Instructions
def add(rd, rs1, rs2):
	registers[rd] = registers[rs1] + registers[rs2]

def sub(rd, rs1, rs2):
	registers[rd] = registers[rs1] - registers[rs2]

def addi(rd, rs1, imm):
	registers[rd] = registers[rs1] + imm

def andi(rd, rs1, imm):
	registers[rd] = registers[rs1] & imm

def ori(rd, rs1, imm):
	registers[rd] = registers[rs1] | imm

def xori(rd, rs1, imm):
	registers[rd] = registers[rs1] ^ imm

def sll(rd, rs1, rs2):
	registers[rd] = registers[rs1] << (registers[rs2] & 0x1F)

	def srl(rd, rs1, rs2):
		registers[rd] =() registers[rs1] & 0xFFFFFFFF) >> (registers[rs2] & 0x1F)

def sra(rd, rs1, rs2):
	registers[rd] = (registers[rs1] >> ((registers[rs2] % 32)+1))&(1<<31)

def slli(rd, rs1, imm):
	registers[rd] = registers[rs1] << imm

def srli(rd, rs1, imm):
	registers[rd] = (registers[rs1] & 0xFFFFFFFF) >> shamt

def srai(rd, rs1, shamt):
	registers[rd] = registers[rs1] >> shamt

def lui(rd, imm):
	registers[rd] = imm << 12

def auipc(rd, imm):
	registers[rd] = imm << 12 + rd

# Comparison Instructions
def slt(rd, rs1, rs2):
	registers[rd] = int(registers[rs1] < registers[rs2])

def sltu(rd, rs1, rs2):
	registers[rd] = int((registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF))

def slti(rd, rs1, imm):
	registers[rd] = int(registers[rs1] < sign_extend(imm, 12))

def sltiu(rd, rs1, imm):
	registers[rd] = int((registers[rs1] & 0xFFFFFFFF) < (sign_extend(imm, 12) & 0xFFFFFFFF))

# Branch Instructions
def beq(rs1, rs2, label):
	if registers[rs1] == registers[rs2]:
		return label

def bne(rs1, rs2, label):
	if registers[rs1] != registers[rs2]:
		return label

def blt(rs1, rs2, label):
	if registers[rs1] < registers[rs2]:
		return label

def bge(rs1, rs2, label):
	if registers[rs1] >= registers[rs2]:
		return label

def bltu(rs1, rs2, label):
	if (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF):
		return label

def bgeu(rs1, rs2, label):
	if (registers[rs1] & 0xFFFFFFFF) >= (registers[rs2] & 0xFFFFFFFF):
		return label

# Load Instructions
def lb(rd, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	registers[rd] = sign_extend(memory.get(addr, 0), 8)

def lh(rd, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	registers[rd] = sign_extend((memory.get(addr, 0) | (memory.get(addr + 1, 0) << 8)), 16)

def lw(rd, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	registers[rd] = memory.get(addr, 0) | (memory.get(addr + 1, 0) << 8) | \
					(memory.get(addr + 2, 0) << 16) | (memory.get(addr + 3, 0) << 24)

def lbu(rd, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	registers[rd] = memory.get(addr, 0) & 0xFF

def lhu(rd, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	registers[rd] = (memory.get(addr, 0) | (memory.get(addr + 1, 0) << 8)) & 0xFFFF

# Store Instructions
def sb(rs2, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	memory[addr] = registers[rs2] & 0xFF

def sh(rs2, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	memory[addr] = registers[rs2] & 0xFF
	memory[addr + 1] = (registers[rs2] >> 8) & 0xFF

def sw(rs2, offset, rs1):
	addr = registers[rs1] + sign_extend(offset, 12)
	memory[addr] = registers[rs2] & 0xFF
	memory[addr + 1] = (registers[rs2] >> 8) & 0xFF
	memory[addr + 2] = (registers[rs2] >> 16) & 0xFF
	memory[addr + 3] = (registers[rs2] >> 24) & 0xFF

# Jump and Link Instructions
def jal(rd, label):
	registers[rd] = label

def jalr(rd, rs1, offset):
	registers[rd] = registers[rs1] + sign_extend(offset, 12)

# Environment Call and Breakpoint
def ecall():
	print("Environment call")

def ebreak():
	print("Breakpoint")

# FENCE Instructions
def fence(pred, succ):
	pass  # Normally affects memory ordering; not simulated here

def fence_i():
	pass  # Normally clears instruction cache

def mul(rd, rs1, rs2):
	registers[rd] = registers[rs1] * registers[rs2]

def div(rd, rs1, rs2):
	registers[rd] = registers[rs1] // registers[rs2] if registers[rs2] != 0 else 0

def rem(rd, rs1, rs2):
	registers[rd] = registers[rs1] % registers[rs2] if registers[rs2] != 0 else 0

