
reg_32 = [0] * 32
ra     = 0
pc     = 0

#1. Load Instructions (I-type)
#These instructions are used to load data from memory into registers:
def LB (): #(Load Byte) #1
    return 
def LH (): #(Load Halfword) #2
    return
def LW (): #(Load Word) #3
    return
def LBU(): # (Load Byte Unsigned) #4
    return
def LHU():  #(Load Halfword Unsigned) #5
    return


#2. Store Instructions (S-type)
#These instructions are used to store data from registers into memory:
def SB(): #(Store Byte) #6
    return
def SH(): #(Store Halfword) #7
    return
def SW(): #(Store Word) #8
    return


#3. Immediate Arithmetic Instructions (I-type)
#These instructions perform arithmetic and logical operations using an immediate value (constant):
def ADDI(rd, rs1, c): #(Add Immediate) #9
    reg_32[rd] = reg_32[rs1] + c

def SLTI(rd, rs1, c): #(Set Less Than Immediate) #10
    if (reg_32[rs1] < c):
        reg_32[rd] = 1
    else:
        reg_32[rd] = 0

def SLTIU(rd, rs1, c): #(Set Less Than Immediate Unsigned) #11
     if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1 

     if (reg_32[rs1] < c):
        reg_32[rd] = 1
     else:
        reg_32[rd] = 0 

def XORI(rd, rs1, c): #(XOR Immediate) #12
    reg_32[rd] = reg_32[rs1] ^ c

def ORI(rd, rs1, c): #(OR Immediate) #13
    reg_32[rd] = reg_32[rs1] | c

def ANDI(rd, rs1, c): #(AND Immediate) #14
     reg_32[rd] = reg_32[rs1] & c

def SLLI(rd, rs1, c): #(Shift Left Logical Immediate) #15
    reg_32[rd] = rs1 << c

def SRLI(rd, rs1, c): #(Shift Right Logical Immediate) #16
    if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1 
        reg_32[rd] = reg_32[rs1]  >> c 
    else:
        reg_32[rd] = reg_32[rs1]  >> c 

def SRAI(rd, rs1, c): #(Shift Right Arithmetic Immediate) #17
     reg_32[rd] = reg_32[rs1]  >> c 


#4. Register-Register Arithmetic Instructions (R-type) 
#These instructions perform arithmetic and logical operations between registers:
def ADD(rd, rs1, rs2): #(Add) #18
    reg_32[rd] = reg_32[rs1] + reg_32[rs2]

def SUB(rd, rs1, rs2): #(Subtract) #19
     reg_32[rd] = reg_32[rs1] - reg_32[rs2]

def SLL(rd, rs1, rs2): #(Shift Left Logical)#20                 
      reg_32[rd] = rs1 << rs2

def SLT(rd, rs1, rs2): #(Set Less Than) #21
    if (reg_32[rs1] < reg_32[rs2]):
        reg_32[rd] = 1
    else:
        reg_32[rd] = 0

def SLTU(rd, rs1, rs2): #(Set Less Than Unsigned )#22
    if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1 

    if (reg_32[rs1] < reg_32[rs2]):
        reg_32[rd] = 1
    else:
        reg_32[rd] = 0 

def XOR(rd, rs1, rs2): #(XOR) #23
     reg_32[rd] = reg_32[rs1] ^ reg_32[rs2]

def SRL(rd, rs1, rs2): #(Shift Right Logical) #24 ///////////////////////////////////////// Not sure need to double check this
    if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1 
        reg_32[rd] = reg_32[rs1]  >> reg_32[rs2] 
    else:
        reg_32[rd] = reg_32[rs1]  >> reg_32[rs2] 

def SRA(rd, rs1, rs2): #(Shift Right Arithmetic) #25
    reg_32[rd] = reg_32[rs1]  >> reg_32[rs2] 

def OR(rd, rs1, rs2): #(OR) #26
     reg_32[rd] = reg_32[rs1] | reg_32[rs2]

def AND(rd ,rs1, rs2): #(AND) #27
     reg_32[rd] = reg_32[rs1] & reg_32[rs2]


#5. Control Flow Instructions (I-type, B-type)
#These instructions control the flow of execution (conditional branches, jumps):
def BEQ(rs1, rs2, offset): #(Branch if Equal) #28
    if (reg_32[rs1] == reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset                                          # ////////////////////////////////???????????????????????????????
       
def BNE(rs1, rs2, offset): #(Branch if Not Equal) #29
    if (reg_32[rs1] != reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset 

def BLT(rs1, rs2, offset): #(Branch if Less Than) #30
    if (reg_32[rs1] < reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset

def BGE(rs1, rs2, offset): #(Branch if Greater Than or Equal) #31
    if (reg_32[rs1] > reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset

def BLTU(rs1, rs2, offset): #(Branch if Less Than Unsigned) #32
    if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1  

    if (reg_32[rs2] < 0 ):
        reg_32[rs2]  = reg_32[rs2]  * -1 

    if (reg_32[rs1] < reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset

def BGEU(rs1, rs2, offset): #(Branch if Greater Than or Equal Unsigned) #33
    if (reg_32[rs1] < 0 ):
        reg_32[rs1]  = reg_32[rs1]  * -1  

    if (reg_32[rs2] < 0 ):
        reg_32[rs2]  = reg_32[rs2]  * -1 

    if (reg_32[rs1] >= reg_32[rs2]):
       ra = pc + 4
       pc = pc + offset


#6. Jumps and Link Instructions (J-type, U-type)
#These instructions are used for jumping to another location in the program:
def JAL(rd, offset): #(Jump and Link) #34
    rd = (pc + offset) & ~1
    ra = pc + 4

def JALR(rd, rs1, c): #(Jump and Link Register) #35
    rd = (rs1 + c) & ~1
    ra = pc + 4


#7. Environment and System Instructions (U-type)
#These instructions are related to the execution environment and control:
def LUI(rd, c): #(Load Upper Immediate) #36
    reg_32[rd] = c << 12

def AUIPC(rd, c): #(Add Upper Immediate to PC) #36
    rd = pc + (c << 12)

#8. Fence and Atomic Instructions
# Halting #1
def FENCE(): #(Fence — synchronize memory accesses) #37
    return

# Halting #2
def FENCE_I(): #(Fence Instruction — invalidate instruction cache) #38
    return

#9. System Instructions (I-type)
#These instructions provide various system-level functionality, including interrupt handling:
# Halting #3
def ECALL(): #(Environment Call — make a system call) #39
    return

# Halting #4
def EBREAK(): #(Environment Break — trigger a breakpoint) #40
    return

# Halting #5
def PAUSE(): #(Environment Break — trigger a breakpoint) #41
    return
def search(label):
    return 

# BONUS 