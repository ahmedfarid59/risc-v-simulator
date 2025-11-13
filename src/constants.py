"""
RISC-V Simulator Constants
Defines supported instructions, register names, and control instructions
"""

# Supported RISC-V instructions
supportedInstructions = [
    'ADD', 'ADDI', 'AND',
    'ANDI', 'AUIPC', 'BEQ',
    'BGE', 'BGEU', 'BLT',
    'BLTU', 'BNE', 'DIV',
    'J', 'JAL', 'JALR',
    'LB', 'LBU', 'LH',
    'LHU', 'LI', 'LUI',
    'LW', 'MUL', 'MV',
    'NEG', 'NOT', 'OR',
    'ORI', 'REM', 'RET',
    'SB', 'SH', 'SLL',
    'SLLI', 'SLT', 'SLTI',
    'SLTIU', 'SLTU', 'SRA',
    'SRAI', 'SRL', 'SRLI',
    'SUB', 'SW', 'XOR',
    'XORI', 'LA'
]

# Dictionary holds the registers alternative names and their x names
regsNames = {
    "zero": "x0",
    "ra": "x1",
    "sp": "x2",
    "gp": "x3",
    "tp": "x4",
    "t0": "x5",
    "t1": "x6",
    "t2": "x7",
    "s0": "x8",
    "fp": "x8",
    "s1": "x9",
    "a0": "x10",
    "a1": "x11",
    "a2": "x12",
    "a3": "x13",
    "a4": "x14",
    "a5": "x15",
    "a6": "x16",
    "a7": "x17",
    "s2": "x18",
    "s3": "x19",
    "s4": "x20",
    "s5": "x21",
    "s6": "x22",
    "s7": "x23",
    "s8": "x24",
    "s9": "x25",
    "s10": "x26",
    "s11": "x27",
    "t3": "x28",
    "t4": "x29",
    "t5": "x30",
    "t6": "x31"
}

# Control and system instructions
system_instructions = ['ECALL', 'EBREAK']
holding = ['PAUSE', 'FENCE', 'FENCE.TSO']

# Memory configuration
DEFAULT_MEMORY_SIZE = 1024  # bytes
MAX_MEMORY_SIZE = 65536  # 64KB

# Register configuration
NUM_REGISTERS = 32
REGISTER_WIDTH = 32  # bits

# Memory layout (Real-world RISC-V addresses)
TEXT_START = 0x00010000      # Code segment
DATA_START = 0x10000000      # Data segment  
HEAP_START = 0x10100000      # Heap segment
STACK_START = 0x7FFFF000     # Stack (grows downward)

# System call numbers (RISC-V Linux ABI)
SYS_EXIT = 93
SYS_WRITE = 64
SYS_READ = 63
