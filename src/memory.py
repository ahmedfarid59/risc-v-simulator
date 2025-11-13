"""
Real-World RISC-V Memory Management System
Implements proper memory segmentation, virtual addressing, and memory-mapped I/O
"""
from .logger import logger
from .constants import *


class MemorySegment:
    """Represents a memory segment with specific permissions and attributes"""
    def __init__(self, start, size, readable=True, writable=True, executable=False, name=""):
        self.start = start
        self.size = size
        self.end = start + size
        self.readable = readable
        self.writable = writable
        self.executable = executable
        self.name = name
        self.data = bytearray(size)
    
    def contains(self, addr):
        """Check if address is within this segment"""
        return self.start <= addr < self.end
    
    def check_access(self, addr, size, write=False, execute=False):
        """Check if access is allowed"""
        if not self.contains(addr):
            return False, f"Address 0x{addr:08X} not in segment {self.name}"
        
        if addr + size > self.end:
            return False, f"Access spans beyond segment {self.name}"
        
        if write and not self.writable:
            return False, f"Write to read-only segment {self.name}"
        
        if execute and not self.executable:
            return False, f"Execution in non-executable segment {self.name}"
        
        if not self.readable and not execute:
            return False, f"Read from non-readable segment {self.name}"
        
        return True, ""
    
    def read(self, addr, size):
        """Read bytes from segment"""
        offset = addr - self.start
        return self.data[offset:offset + size]
    
    def write(self, addr, size, data):
        """Write bytes to segment"""
        offset = addr - self.start
        self.data[offset:offset + size] = data


class Memory:
    """
    Real-world memory management system with segmentation
    Implements standard RISC-V memory layout
    """
    
    # Standard RISC-V memory layout
    TEXT_START = 0x00010000      # Code segment
    TEXT_SIZE = 0x00100000       # 1MB for code
    
    DATA_START = 0x10000000      # Data segment
    DATA_SIZE = 0x00100000       # 1MB for data
    
    HEAP_START = 0x10100000      # Heap segment
    HEAP_SIZE = 0x00100000       # 1MB for heap
    
    STACK_START = 0x7FFFF000     # Stack grows downward
    STACK_SIZE = 0x00100000      # 1MB for stack
    
    MMIO_START = 0xFFFF0000      # Memory-mapped I/O
    MMIO_SIZE = 0x00010000       # 64KB for MMIO
    
    # MMIO addresses
    MMIO_CONSOLE_OUT = 0xFFFF0000    # Console output
    MMIO_CONSOLE_IN = 0xFFFF0004     # Console input
    MMIO_CONSOLE_STATUS = 0xFFFF0008  # Console status
    
    def __init__(self):
        """Initialize memory segments"""
        self.segments = []
        
        # Text segment (code) - readable and executable
        self.text_segment = MemorySegment(
            self.TEXT_START, self.TEXT_SIZE,
            readable=True, writable=False, executable=True,
            name=".text"
        )
        self.segments.append(self.text_segment)
        
        # Data segment - readable and writable
        self.data_segment = MemorySegment(
            self.DATA_START, self.DATA_SIZE,
            readable=True, writable=True, executable=False,
            name=".data"
        )
        self.segments.append(self.data_segment)
        
        # Heap segment - readable and writable
        self.heap_segment = MemorySegment(
            self.HEAP_START, self.HEAP_SIZE,
            readable=True, writable=True, executable=False,
            name=".heap"
        )
        self.segments.append(self.heap_segment)
        self.heap_pointer = self.HEAP_START
        
        # Stack segment - readable and writable
        self.stack_segment = MemorySegment(
            self.STACK_START - self.STACK_SIZE, self.STACK_SIZE,
            readable=True, writable=True, executable=False,
            name=".stack"
        )
        self.segments.append(self.stack_segment)
        
        # Memory-mapped I/O
        self.mmio_segment = MemorySegment(
            self.MMIO_START, self.MMIO_SIZE,
            readable=True, writable=True, executable=False,
            name="MMIO"
        )
        self.segments.append(self.mmio_segment)
        
        # I/O buffers
        self.console_out_buffer = []
        self.console_in_buffer = []
        
        logger.info("Initialized memory management system")
        logger.info(f"  Text:  0x{self.TEXT_START:08X} - 0x{self.TEXT_START + self.TEXT_SIZE:08X}")
        logger.info(f"  Data:  0x{self.DATA_START:08X} - 0x{self.DATA_START + self.DATA_SIZE:08X}")
        logger.info(f"  Heap:  0x{self.HEAP_START:08X} - 0x{self.HEAP_START + self.HEAP_SIZE:08X}")
        logger.info(f"  Stack: 0x{self.STACK_START - self.STACK_SIZE:08X} - 0x{self.STACK_START:08X}")
        logger.info(f"  MMIO:  0x{self.MMIO_START:08X} - 0x{self.MMIO_START + self.MMIO_SIZE:08X}")
    
    def find_segment(self, addr):
        """Find the segment containing the given address"""
        for segment in self.segments:
            if segment.contains(addr):
                return segment
        return None
    
    def read_byte(self, addr):
        """Read a single byte from memory"""
        # Handle MMIO reads
        if self.MMIO_START <= addr < self.MMIO_START + self.MMIO_SIZE:
            return self._mmio_read(addr, 1)
        
        segment = self.find_segment(addr)
        if not segment:
            raise MemoryError(f"Invalid memory read at 0x{addr:08X}")
        
        ok, msg = segment.check_access(addr, 1, write=False)
        if not ok:
            raise MemoryError(msg)
        
        data = segment.read(addr, 1)
        logger.debug(f"Memory read: [0x{addr:08X}] = 0x{data[0]:02X}")
        return data[0]
    
    def read_bytes(self, addr, size):
        """Read multiple bytes from memory"""
        # Handle MMIO reads
        if self.MMIO_START <= addr < self.MMIO_START + self.MMIO_SIZE:
            return self._mmio_read(addr, size)
        
        segment = self.find_segment(addr)
        if not segment:
            raise MemoryError(f"Invalid memory read at 0x{addr:08X}")
        
        ok, msg = segment.check_access(addr, size, write=False)
        if not ok:
            raise MemoryError(msg)
        
        data = segment.read(addr, size)
        logger.debug(f"Memory read: [0x{addr:08X}:{size}] = {data.hex()}")
        return data
    
    def write_byte(self, addr, value):
        """Write a single byte to memory"""
        # Handle MMIO writes
        if self.MMIO_START <= addr < self.MMIO_START + self.MMIO_SIZE:
            self._mmio_write(addr, bytes([value]))
            return
        
        segment = self.find_segment(addr)
        if not segment:
            raise MemoryError(f"Invalid memory write at 0x{addr:08X}")
        
        ok, msg = segment.check_access(addr, 1, write=True)
        if not ok:
            raise MemoryError(msg)
        
        segment.write(addr, 1, bytes([value]))
        logger.debug(f"Memory write: [0x{addr:08X}] = 0x{value:02X}")
    
    def write_bytes(self, addr, data):
        """Write multiple bytes to memory"""
        size = len(data)
        
        # Handle MMIO writes
        if self.MMIO_START <= addr < self.MMIO_START + self.MMIO_SIZE:
            self._mmio_write(addr, data)
            return
        
        segment = self.find_segment(addr)
        if not segment:
            raise MemoryError(f"Invalid memory write at 0x{addr:08X}")
        
        ok, msg = segment.check_access(addr, size, write=True)
        if not ok:
            raise MemoryError(msg)
        
        segment.write(addr, size, data)
        logger.debug(f"Memory write: [0x{addr:08X}:{size}] = {data.hex()}")
    
    def _mmio_read(self, addr, size):
        """Handle memory-mapped I/O reads"""
        if addr == self.MMIO_CONSOLE_STATUS:
            # Return 1 if input available, 0 otherwise
            status = 1 if self.console_in_buffer else 0
            logger.debug(f"MMIO read: Console status = {status}")
            return bytes([status, 0, 0, 0])[:size]
        
        elif addr == self.MMIO_CONSOLE_IN:
            # Read from console input buffer
            if self.console_in_buffer:
                char = self.console_in_buffer.pop(0)
                logger.debug(f"MMIO read: Console input = '{chr(char) if 32 <= char < 127 else f'0x{char:02X}'}'")
                return bytes([char, 0, 0, 0])[:size]
            else:
                return bytes([0] * size)
        
        else:
            # Default MMIO read
            return self.mmio_segment.read(addr, size)
    
    def _mmio_write(self, addr, data):
        """Handle memory-mapped I/O writes"""
        if addr == self.MMIO_CONSOLE_OUT:
            # Write to console output
            char = data[0]
            self.console_out_buffer.append(char)
            if char == ord('\n') or len(self.console_out_buffer) > 80:
                self._flush_console_output()
            logger.debug(f"MMIO write: Console output = '{chr(char) if 32 <= char < 127 else f'0x{char:02X}'}'")
        
        else:
            # Default MMIO write
            self.mmio_segment.write(addr, len(data), data)
    
    def _flush_console_output(self):
        """Flush console output buffer"""
        if self.console_out_buffer:
            text = bytes(self.console_out_buffer).decode('utf-8', errors='replace')
            print(text, end='', flush=True)
            self.console_out_buffer.clear()
    
    def allocate_heap(self, size):
        """Allocate memory on the heap (like malloc)"""
        if self.heap_pointer + size > self.HEAP_START + self.HEAP_SIZE:
            raise MemoryError(f"Heap overflow: cannot allocate {size} bytes")
        
        addr = self.heap_pointer
        self.heap_pointer += size
        logger.info(f"Heap allocation: {size} bytes at 0x{addr:08X}")
        return addr
    
    def load_program_text(self, code_bytes, start_addr=None):
        """Load program code into text segment"""
        if start_addr is None:
            start_addr = self.TEXT_START
        
        size = len(code_bytes)
        if size > self.TEXT_SIZE:
            raise MemoryError(f"Program too large: {size} bytes (max: {self.TEXT_SIZE})")
        
        self.text_segment.write(start_addr, size, code_bytes)
        logger.info(f"Loaded {size} bytes of code at 0x{start_addr:08X}")
        return start_addr
    
    def load_program_data(self, data_bytes, start_addr=None):
        """Load program data into data segment"""
        if start_addr is None:
            start_addr = self.DATA_START
        
        size = len(data_bytes)
        if size > self.DATA_SIZE:
            raise MemoryError(f"Data too large: {size} bytes (max: {self.DATA_SIZE})")
        
        self.data_segment.write(start_addr, size, data_bytes)
        logger.info(f"Loaded {size} bytes of data at 0x{start_addr:08X}")
        return start_addr
    
    def dump_segment(self, segment_name, max_bytes=256):
        """Dump the contents of a memory segment"""
        segment = None
        for seg in self.segments:
            if seg.name == segment_name:
                segment = seg
                break
        
        if not segment:
            return f"Segment '{segment_name}' not found"
        
        output = [f"\n=== {segment.name} Segment (0x{segment.start:08X} - 0x{segment.end:08X}) ==="]
        
        # Find non-zero data
        non_zero = []
        for i, byte in enumerate(segment.data[:max_bytes]):
            if byte != 0:
                non_zero.append((segment.start + i, byte))
        
        if non_zero:
            for addr, value in non_zero:
                output.append(f"  [0x{addr:08X}] = 0x{value:02X} ({value})")
        else:
            output.append("  (all zeros)")
        
        return '\n'.join(output)
    
    def get_stack_pointer(self):
        """Get the initial stack pointer value"""
        return self.STACK_START
    
    def flush_all(self):
        """Flush all output buffers"""
        self._flush_console_output()
