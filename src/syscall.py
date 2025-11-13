"""
RISC-V System Calls Implementation
Implements Linux-like system calls for real-world I/O operations
"""
import sys
import os
from .logger import logger


class SystemCall:
    """
    RISC-V system call handler
    Implements standard Linux RISC-V syscalls
    """
    
    # Standard RISC-V Linux syscall numbers
    SYS_EXIT = 93
    SYS_EXIT_GROUP = 94
    SYS_READ = 63
    SYS_WRITE = 64
    SYS_OPEN = 1024
    SYS_CLOSE = 57
    SYS_LSEEK = 62
    SYS_BRK = 214
    SYS_FSTAT = 80
    SYS_GETPID = 172
    SYS_GETTIMEOFDAY = 169
    
    # Standard file descriptors
    STDIN = 0
    STDOUT = 1
    STDERR = 2
    
    def __init__(self, memory, registers):
        """
        Initialize system call handler
        
        Args:
            memory: Memory management system
            registers: Register file
        """
        self.memory = memory
        self.regs = registers
        self.open_files = {
            self.STDIN: sys.stdin,
            self.STDOUT: sys.stdout,
            self.STDERR: sys.stderr
        }
        self.next_fd = 3
        self.exit_code = 0
        self.should_exit = False
        
        logger.info("Initialized system call handler")
    
    def handle_ecall(self):
        """
        Handle ecall instruction
        
        System call number is in a7 (x17)
        Arguments are in a0-a6 (x10-x16)
        Return value is placed in a0 (x10)
        """
        try:
            # Get syscall number from a7
            syscall_num = self.regs['a7']
            
            logger.info(f"System call: {syscall_num} ({self._get_syscall_name(syscall_num)})")
            
            # Dispatch to appropriate handler
            if syscall_num == self.SYS_EXIT or syscall_num == self.SYS_EXIT_GROUP:
                self._sys_exit()
            elif syscall_num == self.SYS_WRITE:
                self._sys_write()
            elif syscall_num == self.SYS_READ:
                self._sys_read()
            elif syscall_num == self.SYS_OPEN:
                self._sys_open()
            elif syscall_num == self.SYS_CLOSE:
                self._sys_close()
            elif syscall_num == self.SYS_BRK:
                self._sys_brk()
            elif syscall_num == self.SYS_GETPID:
                self._sys_getpid()
            else:
                logger.warning(f"Unimplemented syscall: {syscall_num}")
                self.regs['a0'] = -1  # Return error
        
        except Exception as e:
            logger.error(f"System call error: {e}")
            self.regs['a0'] = -1  # Return error
    
    def _get_syscall_name(self, num):
        """Get syscall name for logging"""
        names = {
            self.SYS_EXIT: "exit",
            self.SYS_EXIT_GROUP: "exit_group",
            self.SYS_READ: "read",
            self.SYS_WRITE: "write",
            self.SYS_OPEN: "open",
            self.SYS_CLOSE: "close",
            self.SYS_LSEEK: "lseek",
            self.SYS_BRK: "brk",
            self.SYS_FSTAT: "fstat",
            self.SYS_GETPID: "getpid",
            self.SYS_GETTIMEOFDAY: "gettimeofday"
        }
        return names.get(num, f"unknown_{num}")
    
    def _sys_exit(self):
        """
        exit(int status)
        Terminate the process
        
        a0: exit status
        """
        self.exit_code = self.regs['a0'] & 0xFF
        self.should_exit = True
        logger.info(f"Program exit with code {self.exit_code}")
        print(f"\n>>> Program exited with status {self.exit_code}")
    
    def _sys_write(self):
        """
        ssize_t write(int fd, const void *buf, size_t count)
        Write to a file descriptor
        
        a0: file descriptor
        a1: buffer address
        a2: count (number of bytes)
        
        Returns: number of bytes written, or -1 on error
        """
        fd = self.regs['a0']
        buf_addr = self.regs['a1']
        count = self.regs['a2']
        
        logger.debug(f"write(fd={fd}, buf=0x{buf_addr:08X}, count={count})")
        
        try:
            # Read data from memory
            data = self.memory.read_bytes(buf_addr, count)
            
            # Write to appropriate file descriptor
            if fd == self.STDOUT or fd == self.STDERR:
                # Write to stdout/stderr
                text = data.decode('utf-8', errors='replace')
                if fd == self.STDOUT:
                    print(text, end='', flush=True)
                else:
                    print(text, end='', file=sys.stderr, flush=True)
                
                logger.info(f"write: {count} bytes to {'stdout' if fd == self.STDOUT else 'stderr'}")
                self.regs['a0'] = count  # Success
            
            elif fd in self.open_files:
                # Write to open file
                file = self.open_files[fd]
                if hasattr(file, 'write'):
                    if isinstance(file, (sys.stdout.__class__, sys.stderr.__class__)):
                        text = data.decode('utf-8', errors='replace')
                        file.write(text)
                    else:
                        file.write(data)
                    file.flush()
                    logger.info(f"write: {count} bytes to fd {fd}")
                    self.regs['a0'] = count  # Success
                else:
                    logger.error(f"write: fd {fd} not writable")
                    self.regs['a0'] = -1  # Error
            
            else:
                logger.error(f"write: invalid fd {fd}")
                self.regs['a0'] = -1  # Error
        
        except Exception as e:
            logger.error(f"write error: {e}")
            self.regs['a0'] = -1  # Error
    
    def _sys_read(self):
        """
        ssize_t read(int fd, void *buf, size_t count)
        Read from a file descriptor
        
        a0: file descriptor
        a1: buffer address
        a2: count (number of bytes)
        
        Returns: number of bytes read, or -1 on error
        """
        fd = self.regs['a0']
        buf_addr = self.regs['a1']
        count = self.regs['a2']
        
        logger.debug(f"read(fd={fd}, buf=0x{buf_addr:08X}, count={count})")
        
        try:
            if fd == self.STDIN:
                # Read from stdin
                data = sys.stdin.read(count)
                bytes_read = len(data)
                data_bytes = data.encode('utf-8')
                
                # Write to memory
                self.memory.write_bytes(buf_addr, data_bytes)
                
                logger.info(f"read: {bytes_read} bytes from stdin")
                self.regs['a0'] = bytes_read  # Success
            
            elif fd in self.open_files:
                # Read from open file
                file = self.open_files[fd]
                if hasattr(file, 'read'):
                    data = file.read(count)
                    if isinstance(data, str):
                        data_bytes = data.encode('utf-8')
                    else:
                        data_bytes = data
                    
                    bytes_read = len(data_bytes)
                    self.memory.write_bytes(buf_addr, data_bytes)
                    
                    logger.info(f"read: {bytes_read} bytes from fd {fd}")
                    self.regs['a0'] = bytes_read  # Success
                else:
                    logger.error(f"read: fd {fd} not readable")
                    self.regs['a0'] = -1  # Error
            
            else:
                logger.error(f"read: invalid fd {fd}")
                self.regs['a0'] = -1  # Error
        
        except Exception as e:
            logger.error(f"read error: {e}")
            self.regs['a0'] = -1  # Error
    
    def _sys_open(self):
        """
        int open(const char *pathname, int flags, mode_t mode)
        Open a file
        
        a0: pathname address
        a1: flags
        a2: mode
        
        Returns: file descriptor, or -1 on error
        """
        pathname_addr = self.regs['a0']
        flags = self.regs['a1']
        mode = self.regs['a2']
        
        try:
            # Read pathname from memory (null-terminated string)
            pathname_bytes = []
            addr = pathname_addr
            while True:
                byte = self.memory.read_byte(addr)
                if byte == 0:
                    break
                pathname_bytes.append(byte)
                addr += 1
                if len(pathname_bytes) > 1024:  # Prevent infinite loop
                    break
            
            pathname = bytes(pathname_bytes).decode('utf-8', errors='replace')
            logger.debug(f"open(pathname='{pathname}', flags=0x{flags:X}, mode=0o{mode:o})")
            
            # Open the file
            # Basic flags: O_RDONLY=0, O_WRONLY=1, O_RDWR=2, O_CREAT=0x40, O_TRUNC=0x200
            mode_str = 'r'
            if flags & 0x1:  # O_WRONLY
                mode_str = 'w'
            elif flags & 0x2:  # O_RDWR
                mode_str = 'r+'
            if flags & 0x40:  # O_CREAT
                mode_str = 'a' if mode_str == 'r' else mode_str
            
            try:
                file = open(pathname, mode_str + 'b')
                fd = self.next_fd
                self.next_fd += 1
                self.open_files[fd] = file
                
                logger.info(f"open: opened '{pathname}' as fd {fd}")
                self.regs['a0'] = fd  # Success
            except FileNotFoundError:
                logger.warning(f"open: file not found '{pathname}'")
                self.regs['a0'] = -1  # Error
        
        except Exception as e:
            logger.error(f"open error: {e}")
            self.regs['a0'] = -1  # Error
    
    def _sys_close(self):
        """
        int close(int fd)
        Close a file descriptor
        
        a0: file descriptor
        
        Returns: 0 on success, -1 on error
        """
        fd = self.regs['a0']
        
        logger.debug(f"close(fd={fd})")
        
        if fd in self.open_files and fd >= 3:  # Don't close stdin/stdout/stderr
            try:
                self.open_files[fd].close()
                del self.open_files[fd]
                logger.info(f"close: closed fd {fd}")
                self.regs['a0'] = 0  # Success
            except Exception as e:
                logger.error(f"close error: {e}")
                self.regs['a0'] = -1  # Error
        else:
            logger.warning(f"close: invalid fd {fd}")
            self.regs['a0'] = -1  # Error
    
    def _sys_brk(self):
        """
        void *brk(void *addr)
        Change the location of the program break (heap)
        
        a0: new break address (or 0 to query current)
        
        Returns: new break address
        """
        new_brk = self.regs['a0']
        
        if new_brk == 0:
            # Query current break
            self.regs['a0'] = self.memory.heap_pointer
            logger.debug(f"brk: query current = 0x{self.memory.heap_pointer:08X}")
        else:
            # Set new break
            if new_brk >= self.memory.HEAP_START and new_brk < self.memory.HEAP_START + self.memory.HEAP_SIZE:
                self.memory.heap_pointer = new_brk
                self.regs['a0'] = new_brk
                logger.info(f"brk: set to 0x{new_brk:08X}")
            else:
                logger.error(f"brk: invalid address 0x{new_brk:08X}")
                self.regs['a0'] = self.memory.heap_pointer  # Return current on error
    
    def _sys_getpid(self):
        """
        pid_t getpid(void)
        Get process ID
        
        Returns: process ID (simulated as 1000)
        """
        self.regs['a0'] = 1000  # Simulated PID
        logger.debug("getpid: returning 1000")
    
    def cleanup(self):
        """Clean up open resources"""
        for fd, file in list(self.open_files.items()):
            if fd >= 3:  # Don't close stdin/stdout/stderr
                try:
                    file.close()
                    logger.debug(f"Cleanup: closed fd {fd}")
                except:
                    pass
