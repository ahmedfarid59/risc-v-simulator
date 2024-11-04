supportedInstructions= [
	# R-type Instructions
	"add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and",
	# I-type Instructions
	"addi", "slti", "sltiu", "xori", "ori", "andi", "slli", "srli", "srai",
	"lb", "lh", "lw", "lbu", "lhu", "jalr",
	# S-type Instructions
	"sb", "sh", "sw",
	# B-type Instructions
	"beq", "bne", "blt", "bge", "bltu", "bgeu",
	# U-type Instructions
	"lui", "auipc",
	# J-type Instructions
	"jal"
]

regsNames= {
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

riscv_registers = {
	"zero": "x0",   # Hardwired zero
	"ra": "x1",     # Return address
	"sp": "x2",     # Stack pointer
	"gp": "x3",     # Global pointer
	"tp": "x4",     # Thread pointer
	"t0": "x5",     # Temporary register 0
	"t1": "x6",     # Temporary register 1
	"t2": "x7",     # Temporary register 2
	"s0": "x8",     # Saved register 0 / frame pointer
	"fp": "x8",     # Alias for s0 (frame pointer)
	"s1": "x9",     # Saved register 1
	"a0": "x10",    # Function argument / return value 0
	"a1": "x11",    # Function argument / return value 1
	"a2": "x12",    # Function argument 2
	"a3": "x13",    # Function argument 3
	"a4": "x14",    # Function argument 4
	"a5": "x15",    # Function argument 5
	"a6": "x16",    # Function argument 6
	"a7": "x17",    # Function argument 7
	"s2": "x18",    # Saved register 2
	"s3": "x19",    # Saved register 3
	"s4": "x20",    # Saved register 4
	"s5": "x21",    # Saved register 5
	"s6": "x22",    # Saved register 6
	"s7": "x23",    # Saved register 7
	"s8": "x24",    # Saved register 8
	"s9": "x25",    # Saved register 9
	"s10": "x26",   # Saved register 10
	"s11": "x27",   # Saved register 11
	"t3": "x28",    # Temporary register 3
	"t4": "x29",    # Temporary register 4
	"t5": "x30",    # Temporary register 5
	"t6": "x31"     # Temporary register 6
}
