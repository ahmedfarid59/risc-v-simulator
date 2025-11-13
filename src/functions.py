"""
RISC-V Instruction Implementation
Implements all supported RISC-V instructions with logging and error handling
"""
from .registers import registers, RegisterError
from .logger import logger
from .constants import *
from .utils import ExecutionError, sign_extend

# Global state - will be initialized by simulator
regs = None
memory = None
csr = None
syscall = None
pc = 0
labels = {}
vars = {}


def check_memory_bounds(addr, size, operation="access"):
    """
    Check if memory access is within bounds
    
    Args:
        addr: Memory address
        size: Number of bytes to access
        operation: Type of operation (for error message)
    
    Raises:
        ExecutionError: If access is out of bounds
    """
    if addr < 0:
        raise ExecutionError(f"Negative memory address: {addr}")
    
    # Memory bounds checking is now handled by Memory class
    logger.debug(f"Memory {operation} at 0x{addr:08X}, size={size} bytes")

# ============================================================================
# Arithmetic and Logic Instructions
# ============================================================================

def ADD(rd, rs1, rs2):
    """Add: rd = rs1 + rs2"""
    try:
        result = (regs[rs1] + regs[rs2]) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"ADD {rd}, {rs1}, {rs2}: {regs[rs1]} + {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"ADD execution error: {e}")
        raise


def SUB(rd, rs1, rs2):
    """Subtract: rd = rs1 - rs2"""
    try:
        result = (regs[rs1] - regs[rs2]) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"SUB {rd}, {rs1}, {rs2}: {regs[rs1]} - {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SUB execution error: {e}")
        raise


def ADDI(rd, rs1, imm):
    """Add Immediate: rd = rs1 + imm"""
    try:
        imm_val = sign_extend(imm, 12)
        result = (regs[rs1] + imm_val) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"ADDI {rd}, {rs1}, {imm}: {regs[rs1]} + {imm_val} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"ADDI execution error: {e}")
        raise


def AND(rd, rs1, rs2):
    """Bitwise AND: rd = rs1 & rs2"""
    try:
        result = regs[rs1] & regs[rs2]
        regs[rd] = result
        logger.info(f"AND {rd}, {rs1}, {rs2}: {regs[rs1]} & {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"AND execution error: {e}")
        raise


def ANDI(rd, rs1, imm):
    """Bitwise AND Immediate: rd = rs1 & imm"""
    try:
        imm_val = sign_extend(imm, 12)
        result = regs[rs1] & imm_val
        regs[rd] = result
        logger.info(f"ANDI {rd}, {rs1}, {imm}: {regs[rs1]} & {imm_val} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"ANDI execution error: {e}")
        raise


def OR(rd, rs1, rs2):
    """Bitwise OR: rd = rs1 | rs2"""
    try:
        result = regs[rs1] | regs[rs2]
        regs[rd] = result
        logger.info(f"OR {rd}, {rs1}, {rs2}: {regs[rs1]} | {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"OR execution error: {e}")
        raise


def ORI(rd, rs1, imm):
    """Bitwise OR Immediate: rd = rs1 | imm"""
    try:
        imm_val = sign_extend(imm, 12)
        result = regs[rs1] | imm_val
        regs[rd] = result
        logger.info(f"ORI {rd}, {rs1}, {imm}: {regs[rs1]} | {imm_val} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"ORI execution error: {e}")
        raise


def XOR(rd, rs1, rs2):
    """Bitwise XOR: rd = rs1 ^ rs2"""
    try:
        result = regs[rs1] ^ regs[rs2]
        regs[rd] = result
        logger.info(f"XOR {rd}, {rs1}, {rs2}: {regs[rs1]} ^ {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"XOR execution error: {e}")
        raise


def XORI(rd, rs1, imm):
    """Bitwise XOR Immediate: rd = rs1 ^ imm"""
    try:
        imm_val = sign_extend(imm, 12)
        result = regs[rs1] ^ imm_val
        regs[rd] = result
        logger.info(f"XORI {rd}, {rs1}, {imm}: {regs[rs1]} ^ {imm_val} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"XORI execution error: {e}")
        raise

# ============================================================================
# Shift Instructions
# ============================================================================

def SLLI(rd, rs1, imm):
    """Shift Left Logical Immediate: rd = rs1 << imm"""
    try:
        shift = int(imm) & 0x1F
        result = (regs[rs1] << shift) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"SLLI {rd}, {rs1}, {imm}: {regs[rs1]} << {shift} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLLI execution error: {e}")
        raise


def SRLI(rd, rs1, imm):
    """Shift Right Logical Immediate: rd = rs1 >> imm (unsigned)"""
    try:
        shift = int(imm) & 0x1F
        result = (regs[rs1] & 0xFFFFFFFF) >> shift
        regs[rd] = result
        logger.info(f"SRLI {rd}, {rs1}, {imm}: {regs[rs1]} >> {shift} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SRLI execution error: {e}")
        raise


def SLL(rd, rs1, rs2):
    """Shift Left Logical: rd = rs1 << rs2"""
    try:
        shift = regs[rs2] & 0x1F
        result = (regs[rs1] << shift) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"SLL {rd}, {rs1}, {rs2}: {regs[rs1]} << {shift} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLL execution error: {e}")
        raise


def SRL(rd, rs1, rs2):
    """Shift Right Logical: rd = rs1 >> rs2 (unsigned)"""
    try:
        shift = regs[rs2] & 0x1F
        result = (regs[rs1] & 0xFFFFFFFF) >> shift
        regs[rd] = result
        logger.info(f"SRL {rd}, {rs1}, {rs2}: {regs[rs1]} >> {shift} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SRL execution error: {e}")
        raise


def SRA(rd, rs1, rs2):
    """Shift Right Arithmetic: rd = rs1 >> rs2 (signed)"""
    try:
        value = regs[rs1]
        shift = regs[rs2] & 0x1F
        
        # Arithmetic right shift: preserve sign bit
        if value & 0x80000000:  # negative
            result = (value >> shift) | ((0xFFFFFFFF << (32 - shift)) & 0xFFFFFFFF)
        else:  # positive
            result = value >> shift
        
        regs[rd] = result
        logger.info(f"SRA {rd}, {rs1}, {rs2}: {value} >> {shift} = {result} (arithmetic)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SRA execution error: {e}")
        raise


def SRAI(rd, rs1, imm):
    """Shift Right Arithmetic Immediate: rd = rs1 >> imm (signed)"""
    try:
        value = regs[rs1]
        shift = int(imm) & 0x1F
        
        # Arithmetic right shift: preserve sign bit
        if value & 0x80000000:  # negative
            result = (value >> shift) | ((0xFFFFFFFF << (32 - shift)) & 0xFFFFFFFF)
        else:  # positive
            result = value >> shift
        
        regs[rd] = result
        logger.info(f"SRAI {rd}, {rs1}, {imm}: {value} >> {shift} = {result} (arithmetic)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SRAI execution error: {e}")
        raise

# ============================================================================
# Comparison Instructions
# ============================================================================

def SLT(rd, rs1, rs2):
    """Set Less Than: rd = (rs1 < rs2) ? 1 : 0 (signed)"""
    try:
        # Signed comparison
        val1 = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
        val2 = regs[rs2] if regs[rs2] < 0x80000000 else regs[rs2] - 0x100000000
        result = int(val1 < val2)
        regs[rd] = result
        logger.info(f"SLT {rd}, {rs1}, {rs2}: {val1} < {val2} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLT execution error: {e}")
        raise


def SLTU(rd, rs1, rs2):
    """Set Less Than Unsigned: rd = (rs1 < rs2) ? 1 : 0 (unsigned)"""
    try:
        # Unsigned comparison
        val1 = regs[rs1] & 0xFFFFFFFF
        val2 = regs[rs2] & 0xFFFFFFFF
        result = int(val1 < val2)
        regs[rd] = result
        logger.info(f"SLTU {rd}, {rs1}, {rs2}: {val1} < {val2} = {result} (unsigned)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLTU execution error: {e}")
        raise


def SLTI(rd, rs1, imm):
    """Set Less Than Immediate: rd = (rs1 < imm) ? 1 : 0 (signed)"""
    try:
        imm_val = sign_extend(imm, 12)
        val1 = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
        result = int(val1 < imm_val)
        regs[rd] = result
        logger.info(f"SLTI {rd}, {rs1}, {imm}: {val1} < {imm_val} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLTI execution error: {e}")
        raise


def SLTIU(rd, rs1, imm):
    """Set Less Than Immediate Unsigned: rd = (rs1 < imm) ? 1 : 0 (unsigned)"""
    try:
        imm_val = sign_extend(imm, 12) & 0xFFFFFFFF
        val1 = regs[rs1] & 0xFFFFFFFF
        result = int(val1 < imm_val)
        regs[rd] = result
        logger.info(f"SLTIU {rd}, {rs1}, {imm}: {val1} < {imm_val} = {result} (unsigned)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SLTIU execution error: {e}")
        raise

# ============================================================================
# Branch Instructions
# ============================================================================

def BEQ(rs1, rs2, label):
    """Branch if Equal: if (rs1 == rs2) pc = label"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        if regs[rs1] == regs[rs2]:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BEQ {rs1}, {rs2}, {label}: taken (branch to {labels[label]})")
        else:
            logger.info(f"BEQ {rs1}, {rs2}, {label}: not taken")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BEQ execution error: {e}")
        raise


def BNE(rs1, rs2, label):
    """Branch if Not Equal: if (rs1 != rs2) pc = label"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        if regs[rs1] != regs[rs2]:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BNE {rs1}, {rs2}, {label}: taken (branch to {labels[label]})")
        else:
            logger.info(f"BNE {rs1}, {rs2}, {label}: not taken")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BNE execution error: {e}")
        raise


def BLT(rs1, rs2, label):
    """Branch if Less Than: if (rs1 < rs2) pc = label (signed)"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        val1 = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
        val2 = regs[rs2] if regs[rs2] < 0x80000000 else regs[rs2] - 0x100000000
        
        if val1 < val2:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BLT {rs1}, {rs2}, {label}: taken ({val1} < {val2})")
        else:
            logger.info(f"BLT {rs1}, {rs2}, {label}: not taken ({val1} >= {val2})")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BLT execution error: {e}")
        raise


def BGE(rs1, rs2, label):
    """Branch if Greater or Equal: if (rs1 >= rs2) pc = label (signed)"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        val1 = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
        val2 = regs[rs2] if regs[rs2] < 0x80000000 else regs[rs2] - 0x100000000
        
        if val1 >= val2:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BGE {rs1}, {rs2}, {label}: taken ({val1} >= {val2})")
        else:
            logger.info(f"BGE {rs1}, {rs2}, {label}: not taken ({val1} < {val2})")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BGE execution error: {e}")
        raise


def BLTU(rs1, rs2, label):
    """Branch if Less Than Unsigned: if (rs1 < rs2) pc = label (unsigned)"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        val1 = regs[rs1] & 0xFFFFFFFF
        val2 = regs[rs2] & 0xFFFFFFFF
        
        if val1 < val2:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BLTU {rs1}, {rs2}, {label}: taken ({val1} < {val2}, unsigned)")
        else:
            logger.info(f"BLTU {rs1}, {rs2}, {label}: not taken ({val1} >= {val2}, unsigned)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BLTU execution error: {e}")
        raise


def BGEU(rs1, rs2, label):
    """Branch if Greater or Equal Unsigned: if (rs1 >= rs2) pc = label (unsigned)"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        val1 = regs[rs1] & 0xFFFFFFFF
        val2 = regs[rs2] & 0xFFFFFFFF
        
        if val1 >= val2:
            pc = labels[label] - 1  # -1 because main loop will increment
            logger.info(f"BGEU {rs1}, {rs2}, {label}: taken ({val1} >= {val2}, unsigned)")
        else:
            logger.info(f"BGEU {rs1}, {rs2}, {label}: not taken ({val1} < {val2}, unsigned)")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"BGEU execution error: {e}")
        raise

# ============================================================================
# Load Instructions
# ============================================================================

def LB(rd, offset, rs1):
    """Load Byte: rd = sign_extend(memory[rs1 + offset][7:0])"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 1, "load byte")
        
        data = memory.read_bytes(addr, 1)
        value = int.from_bytes(data, byteorder='big', signed=True)
        regs[rd] = value & 0xFFFFFFFF
        logger.info(f"LB {rd}, {offset}({rs1}): loaded {value} from address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LB execution error: {e}")
        raise


def LH(rd, offset, rs1):
    """Load Halfword: rd = sign_extend(memory[rs1 + offset][15:0])"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 2, "load halfword")
        
        data = memory.read_bytes(addr, 2)
        value = int.from_bytes(data, byteorder='big', signed=True)
        regs[rd] = value & 0xFFFFFFFF
        logger.info(f"LH {rd}, {offset}({rs1}): loaded {value} from address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LH execution error: {e}")
        raise


def LW(rd, offset, rs1):
    """Load Word: rd = memory[rs1 + offset][31:0]"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 4, "load word")
        
        data = memory.read_bytes(addr, 4)
        value = int.from_bytes(data, byteorder='big', signed=True)
        regs[rd] = value & 0xFFFFFFFF
        logger.info(f"LW {rd}, {offset}({rs1}): loaded {value} from address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LW execution error: {e}")
        raise


def LBU(rd, offset, rs1):
    """Load Byte Unsigned: rd = zero_extend(memory[rs1 + offset][7:0])"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 1, "load byte unsigned")
        
        data = memory.read_bytes(addr, 1)
        value = int.from_bytes(data, byteorder='big', signed=False)
        regs[rd] = value
        logger.info(f"LBU {rd}, {offset}({rs1}): loaded {value} from address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LBU execution error: {e}")
        raise


def LHU(rd, offset, rs1):
    """Load Halfword Unsigned: rd = zero_extend(memory[rs1 + offset][15:0])"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 2, "load halfword unsigned")
        
        data = memory.read_bytes(addr, 2)
        value = int.from_bytes(data, byteorder='big', signed=False)
        regs[rd] = value
        logger.info(f"LHU {rd}, {offset}({rs1}): loaded {value} from address 0x{addr:04X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LHU execution error: {e}")
        raise

def AUIPC(rd, imm):
    """Add Upper Immediate to PC: rd = pc + (imm << 12)"""
    try:
        from .utils import parse_immediate
        imm_val = parse_immediate(imm) if isinstance(imm, str) else int(imm)
        result = ((imm_val << 12) + pc) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"AUIPC {rd}, {imm}: {pc} + {imm_val << 12} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"AUIPC execution error: {e}")
        raise


def LUI(rd, imm):
    """Load Upper Immediate: rd = imm << 12"""
    try:
        from .utils import parse_immediate
        imm_val = parse_immediate(imm) if isinstance(imm, str) else int(imm)
        result = (imm_val << 12) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"LUI {rd}, {imm}: {imm_val} << 12 = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LUI execution error: {e}")
        raise


# ============================================================================
# Store Instructions
# ============================================================================

def SB(rs2, offset, rs1):
    """Store Byte: memory[rs1 + offset] = rs2[7:0]"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 1, "store byte")
        
        value = regs[rs2] & 0xFF
        data = value.to_bytes(1, byteorder='big')
        memory.write_bytes(addr, data)
        logger.info(f"SB {rs2}, {offset}({rs1}): stored {value} at address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SB execution error: {e}")
        raise


def SH(rs2, offset, rs1):
    """Store Halfword: memory[rs1 + offset] = rs2[15:0]"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 2, "store halfword")
        
        value = regs[rs2] & 0xFFFF
        data = value.to_bytes(2, byteorder='big')
        memory.write_bytes(addr, data)
        logger.info(f"SH {rs2}, {offset}({rs1}): stored {value} at address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SH execution error: {e}")
        raise


def SW(rs2, offset, rs1):
    """Store Word: memory[rs1 + offset] = rs2[31:0]"""
    try:
        addr = regs[rs1] + sign_extend(offset, 12)
        check_memory_bounds(addr, 4, "store word")
        
        value = regs[rs2] & 0xFFFFFFFF
        data = value.to_bytes(4, byteorder='big')
        memory.write_bytes(addr, data)
        logger.info(f"SW {rs2}, {offset}({rs1}): stored {value} at address 0x{addr:08X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"SW execution error: {e}")
        raise

# ============================================================================
# Jump Instructions
# ============================================================================

def JAL(rd, label):
    """Jump and Link: rd = pc + 1, pc = label"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        regs[rd] = pc + 1  # Store return address (next instruction)
        pc = labels[label] - 1  # -1 because main loop will increment
        logger.info(f"JAL {rd}, {label}: jump to {labels[label]}, return address = {pc + 2}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"JAL execution error: {e}")
        raise


def JALR(rd, rs1, offset):
    """Jump and Link Register: rd = pc + 1, pc = rs1 + offset"""
    global pc
    try:
        offset_val = sign_extend(offset, 12)
        target = (regs[rs1] + offset_val) & 0xFFFFFFFE  # Clear LSB for alignment
        
        regs[rd] = pc + 1  # Store return address (next instruction)
        pc = target - 1  # -1 because main loop will increment
        logger.info(f"JALR {rd}, {offset}({rs1}): jump to {target}, return address = {pc + 2}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"JALR execution error: {e}")
        raise


def J(label):
    """Jump: pc = label"""
    global pc
    try:
        if label not in labels:
            raise ExecutionError(f"Undefined label: {label}")
        
        pc = labels[label] - 1  # -1 because main loop will increment
        logger.info(f"J {label}: jump to {labels[label]}")
    except ExecutionError as e:
        logger.error(f"J execution error: {e}")
        raise


def RET():
    """Return: pc = ra"""
    global pc
    try:
        pc = regs['x1'] - 1  # Return address is already next instruction
        logger.info(f"RET: returning to address {pc + 1}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"RET execution error: {e}")
        raise


# ============================================================================
# Multiplication and Division Instructions
# ============================================================================

def MUL(rd, rs1, rs2):
    """Multiply: rd = (rs1 * rs2)[31:0]"""
    try:
        result = (regs[rs1] * regs[rs2]) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"MUL {rd}, {rs1}, {rs2}: {regs[rs1]} * {regs[rs2]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"MUL execution error: {e}")
        raise


def DIV(rd, rs1, rs2):
    """Divide: rd = rs1 / rs2 (signed, round toward zero)"""
    try:
        divisor = regs[rs2]
        if divisor == 0:
            result = 0xFFFFFFFF  # Division by zero result
            logger.warning(f"DIV {rd}, {rs1}, {rs2}: division by zero, result = -1")
        else:
            # Signed division
            dividend = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
            divisor_signed = divisor if divisor < 0x80000000 else divisor - 0x100000000
            result = int(dividend / divisor_signed) & 0xFFFFFFFF
            logger.info(f"DIV {rd}, {rs1}, {rs2}: {dividend} / {divisor_signed} = {result}")
        
        regs[rd] = result
    except (RegisterError, ExecutionError) as e:
        logger.error(f"DIV execution error: {e}")
        raise


def REM(rd, rs1, rs2):
    """Remainder: rd = rs1 % rs2 (signed)"""
    try:
        divisor = regs[rs2]
        if divisor == 0:
            result = regs[rs1]  # Remainder by zero returns dividend
            logger.warning(f"REM {rd}, {rs1}, {rs2}: remainder by zero, result = dividend")
        else:
            # Signed remainder
            dividend = regs[rs1] if regs[rs1] < 0x80000000 else regs[rs1] - 0x100000000
            divisor_signed = divisor if divisor < 0x80000000 else divisor - 0x100000000
            result = (dividend % divisor_signed) & 0xFFFFFFFF
            logger.info(f"REM {rd}, {rs1}, {rs2}: {dividend} % {divisor_signed} = {result}")
        
        regs[rd] = result
    except (RegisterError, ExecutionError) as e:
        logger.error(f"REM execution error: {e}")
        raise


# ============================================================================
# Pseudo-instructions
# ============================================================================

def MV(rd, rs):
    """Move: rd = rs (pseudo-instruction for ADDI rd, rs, 0)"""
    try:
        regs[rd] = regs[rs]
        logger.info(f"MV {rd}, {rs}: {regs[rs]} copied to {rd}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"MV execution error: {e}")
        raise


def NOT(rd, rs):
    """Bitwise NOT: rd = ~rs (pseudo-instruction for XORI rd, rs, -1)"""
    try:
        result = (~regs[rs]) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"NOT {rd}, {rs}: ~{regs[rs]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"NOT execution error: {e}")
        raise


def NEG(rd, rs):
    """Negate: rd = -rs (pseudo-instruction for SUB rd, x0, rs)"""
    try:
        result = (-regs[rs]) & 0xFFFFFFFF
        regs[rd] = result
        logger.info(f"NEG {rd}, {rs}: -{regs[rs]} = {result}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"NEG execution error: {e}")
        raise


def LI(rd, imm):
    """Load Immediate: rd = imm (pseudo-instruction)"""
    try:
        value = sign_extend(imm, 32) if isinstance(imm, int) and abs(int(imm)) <= 2047 else int(imm)
        regs[rd] = value & 0xFFFFFFFF
        logger.info(f"LI {rd}, {imm}: loaded {value}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LI execution error: {e}")
        raise


def LA(rd, var):
    """Load Address: rd = address of var"""
    try:
        # Check both variables (data section) and labels (text section)
        if var in vars:
            addr = vars[var]
        elif var in labels:
            addr = labels[var]
        else:
            raise ExecutionError(f"Undefined variable or label: {var}")
        
        regs[rd] = addr
        logger.info(f"LA {rd}, {var}: loaded address 0x{addr:04X}")
    except (RegisterError, ExecutionError) as e:
        logger.error(f"LA execution error: {e}")
        raise
