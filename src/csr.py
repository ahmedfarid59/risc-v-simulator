"""
RISC-V Control and Status Registers (CSR)
Implements system-level state and control
"""
from .logger import logger


class CSRRegister:
    """Control and Status Register implementation"""
    
    # CSR addresses (standard RISC-V)
    # Machine Information Registers
    MVENDORID = 0xF11   # Vendor ID
    MARCHID = 0xF12     # Architecture ID
    MIMPID = 0xF13      # Implementation ID
    MHARTID = 0xF14     # Hardware thread ID
    
    # Machine Trap Setup
    MSTATUS = 0x300     # Machine status register
    MISA = 0x301        # ISA and extensions
    MEDELEG = 0x302     # Exception delegation
    MIDELEG = 0x303     # Interrupt delegation
    MIE = 0x304         # Interrupt enable
    MTVEC = 0x305       # Trap vector base address
    
    # Machine Trap Handling
    MSCRATCH = 0x340    # Scratch register
    MEPC = 0x341        # Exception program counter
    MCAUSE = 0x342      # Trap cause
    MTVAL = 0x343       # Trap value
    MIP = 0x344         # Interrupt pending
    
    # Machine Counter/Timers
    MCYCLE = 0xB00      # Cycle counter
    MTIME = 0xB01       # Time counter
    MINSTRET = 0xB02    # Instructions retired
    
    # User-level CSRs
    CYCLE = 0xC00       # Cycle counter (user read-only)
    TIME = 0xC01        # Time counter (user read-only)
    INSTRET = 0xC02     # Instructions retired (user read-only)
    
    # Exception causes
    CAUSE_INSTRUCTION_MISALIGNED = 0
    CAUSE_INSTRUCTION_ACCESS_FAULT = 1
    CAUSE_ILLEGAL_INSTRUCTION = 2
    CAUSE_BREAKPOINT = 3
    CAUSE_LOAD_MISALIGNED = 4
    CAUSE_LOAD_ACCESS_FAULT = 5
    CAUSE_STORE_MISALIGNED = 6
    CAUSE_STORE_ACCESS_FAULT = 7
    CAUSE_ECALL_FROM_U = 8
    CAUSE_ECALL_FROM_M = 11
    
    def __init__(self):
        """Initialize CSR registers"""
        self.registers = {}
        
        # Initialize standard CSRs
        self.registers[self.MVENDORID] = 0x0      # Open source implementation
        self.registers[self.MARCHID] = 0x0        # Architecture ID
        self.registers[self.MIMPID] = 0x01000000  # Implementation version 1.0
        self.registers[self.MHARTID] = 0x0        # Hardware thread 0
        
        self.registers[self.MSTATUS] = 0x00000000  # Machine status
        self.registers[self.MISA] = 0x40000100     # RV32I
        self.registers[self.MIE] = 0x0             # Interrupts disabled
        self.registers[self.MTVEC] = 0x0           # Trap vector
        
        self.registers[self.MSCRATCH] = 0x0
        self.registers[self.MEPC] = 0x0
        self.registers[self.MCAUSE] = 0x0
        self.registers[self.MTVAL] = 0x0
        self.registers[self.MIP] = 0x0
        
        self.registers[self.MCYCLE] = 0x0
        self.registers[self.MTIME] = 0x0
        self.registers[self.MINSTRET] = 0x0
        
        logger.info("Initialized CSR registers")
    
    def read(self, addr):
        """Read from CSR"""
        # Map user-level counters to machine-level
        if addr == self.CYCLE:
            addr = self.MCYCLE
        elif addr == self.TIME:
            addr = self.MTIME
        elif addr == self.INSTRET:
            addr = self.MINSTRET
        
        if addr in self.registers:
            value = self.registers[addr]
            logger.debug(f"CSR read: [0x{addr:03X}] = 0x{value:08X}")
            return value
        else:
            logger.warning(f"CSR read from undefined register: 0x{addr:03X}")
            return 0
    
    def write(self, addr, value):
        """Write to CSR"""
        # Some CSRs are read-only
        read_only = [self.MVENDORID, self.MARCHID, self.MIMPID, self.MHARTID,
                     self.CYCLE, self.TIME, self.INSTRET]
        
        if addr in read_only:
            logger.warning(f"CSR write to read-only register: 0x{addr:03X}")
            return
        
        if addr in self.registers:
            old_value = self.registers[addr]
            self.registers[addr] = value & 0xFFFFFFFF
            logger.debug(f"CSR write: [0x{addr:03X}] = 0x{value:08X} (was 0x{old_value:08X})")
        else:
            logger.warning(f"CSR write to undefined register: 0x{addr:03X}")
    
    def increment_cycle(self):
        """Increment cycle counter"""
        self.registers[self.MCYCLE] = (self.registers[self.MCYCLE] + 1) & 0xFFFFFFFF
    
    def increment_instret(self):
        """Increment instructions retired counter"""
        self.registers[self.MINSTRET] = (self.registers[self.MINSTRET] + 1) & 0xFFFFFFFF
    
    def set_exception(self, cause, pc, tval=0):
        """Set exception state"""
        self.registers[self.MCAUSE] = cause
        self.registers[self.MEPC] = pc
        self.registers[self.MTVAL] = tval
        logger.info(f"Exception: cause={cause}, pc=0x{pc:08X}, tval=0x{tval:08X}")
    
    def get_trap_vector(self):
        """Get trap handler address"""
        return self.registers[self.MTVEC]
    
    def dump(self):
        """Dump CSR state"""
        output = ["\n=== Control and Status Registers ==="]
        
        important_csrs = [
            (self.MHARTID, "mhartid"),
            (self.MSTATUS, "mstatus"),
            (self.MISA, "misa"),
            (self.MIE, "mie"),
            (self.MTVEC, "mtvec"),
            (self.MEPC, "mepc"),
            (self.MCAUSE, "mcause"),
            (self.MTVAL, "mtval"),
            (self.MCYCLE, "mcycle"),
            (self.MINSTRET, "minstret"),
        ]
        
        for addr, name in important_csrs:
            if addr in self.registers:
                value = self.registers[addr]
                output.append(f"  {name:12} (0x{addr:03X}) = 0x{value:08X} ({value})")
        
        return '\n'.join(output)
