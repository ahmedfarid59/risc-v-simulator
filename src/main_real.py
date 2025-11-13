"""
Real-World RISC-V Simulator - Main Entry Point
Full-featured simulator with proper memory management, system calls, and CSRs
"""
import sys
import argparse
from .logger import logger, setup_logger
from .memory import Memory
from .registers import registers
from .csr import CSRRegister
from .syscall import SystemCall
from .constants import *


class RISCVSimulator:
    """
    Real-world RISC-V simulator with proper architecture
    """
    
    def __init__(self):
        """Initialize the simulator"""
        # Initialize components
        logger.info("="*80)
        logger.info("Initializing Real-World RISC-V Simulator")
        logger.info("="*80)
        
        self.memory = Memory()
        self.regs = registers()
        self.csr = CSRRegister()
        self.syscall = SystemCall(self.memory, self.regs)
        
        self.pc = self.memory.TEXT_START
        self.instructions = []
        self.labels = {}
        self.vars_map = {}
        
        # Initialize stack pointer (use x2, which is sp)
        self.regs['x2'] = self.memory.get_stack_pointer()
        logger.info(f"Stack pointer initialized to 0x{self.regs['x2']:08X}")
        
        logger.info("Simulator initialized successfully")
    
    def load_program(self, asm_file):
        """
        Load and parse a RISC-V assembly program
        
        Args:
            asm_file: Path to assembly file
        
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Loading program: {asm_file}")
            
            # Import parser
            from .parse_real import parse_program
            
            # Parse the program (pass memory object)
            success, instructions, labels, data, vars_map = parse_program(asm_file, self.memory)
            
            if not success:
                logger.error("Failed to parse program")
                return False
            
            self.instructions = instructions
            self.labels = labels
            self.vars_map = vars_map
            
            # Load data into memory
            if data:
                self.memory.load_program_data(data, self.memory.DATA_START)
            
            logger.info(f"Loaded {len(instructions)} instructions")
            logger.info(f"Found {len(labels)} labels: {list(labels.keys())}")
            logger.info(f"Found {len(vars_map)} variables: {list(vars_map.keys())}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading program: {e}")
            return False
    
    def run(self, max_instructions=100000):
        """
        Run the loaded program
        
        Args:
            max_instructions: Maximum instructions to prevent infinite loops
        
        Returns:
            int: Exit code
        """
        logger.info("="*80)
        logger.info("Starting program execution")
        logger.info(f"Entry point: 0x{self.pc:08X}")
        logger.info("="*80)
        
        instruction_count = 0
        instruction_index = 0
        
        try:
            while instruction_index < len(self.instructions) and instruction_count < max_instructions:
                # Get current instruction
                if instruction_index < 0 or instruction_index >= len(self.instructions):
                    logger.error(f"PC out of bounds: {instruction_index}")
                    break
                
                ins = self.instructions[instruction_index]
                
                # Skip empty or label-only instructions
                if not ins or (isinstance(ins, list) and len(ins) > 0 and ins[0].endswith(':')):
                    instruction_index += 1
                    continue
                
                # Execute instruction
                opcode = ins[0] if isinstance(ins, list) else ins
                
                # Handle system calls
                if opcode == 'ECALL':
                    self.syscall.handle_ecall()
                    if self.syscall.should_exit:
                        logger.info(f"Program requested exit with code {self.syscall.exit_code}")
                        break
                else:
                    # Execute the instruction
                    try:
                        result = self._execute_instruction(ins, instruction_index)
                        if result is not None:
                            # Instruction modified PC (jump/branch)
                            instruction_index = result
                            continue
                    except Exception as e:
                        logger.error(f"Error executing instruction {ins}: {e}")
                        raise
                
                # Increment counters
                self.csr.increment_cycle()
                self.csr.increment_instret()
                instruction_count += 1
                instruction_index += 1
            
            # Check for timeout
            if instruction_count >= max_instructions:
                logger.warning(f"Maximum instruction count reached ({max_instructions})")
                
            # Flush output
            self.memory.flush_all()
            
            logger.info("="*80)
            logger.info(f"Execution completed: {instruction_count} instructions")
            logger.info(f"Exit code: {self.syscall.exit_code}")
            logger.info("="*80)
            
            return self.syscall.exit_code
            
        except KeyboardInterrupt:
            logger.info("Execution interrupted by user")
            return 130
            
        except Exception as e:
            logger.exception(f"Fatal error during execution: {e}")
            return 1
        
        finally:
            self.syscall.cleanup()
    
    def _execute_instruction(self, ins, pc):
        """
        Execute a single instruction
        
        Args:
            ins: Instruction tokens [opcode, operands...]
            pc: Current program counter
            
        Returns:
            New PC if jump/branch, None otherwise
        """
        from . import functions
        
        # Set up global references for functions module
        # Always update to ensure we're using the current simulator instance
        functions.regs = self.regs
        functions.memory = self.memory
        functions.csr = self.csr
        functions.syscall = self.syscall
        functions.pc = pc
        functions.labels = self.labels
        functions.vars = self.vars_map
        
        opcode = ins[0].upper()
        operands = ins[1:] if len(ins) > 1 else []
        
        # Normalize operands to uppercase for register names
        operands = [op.upper() if isinstance(op, str) else op for op in operands]
        
        # Get the instruction function
        if hasattr(functions, opcode):
            func = getattr(functions, opcode)
            
            try:
                # Call the function with operands
                result = func(*operands)
                
                # Check if it's a jump/branch that returns new PC
                if result is not None and opcode in ['JAL', 'JALR', 'BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']:
                    return result
                    
            except Exception as e:
                logger.error(f"Error in {opcode} with operands {operands}: {e}")
                raise
        else:
            logger.warning(f"Unsupported instruction: {opcode}")
        
        return None


def main():
    """Main entry point for command-line usage"""
    parser = argparse.ArgumentParser(description='RISC-V Simulator')
    parser.add_argument('file', nargs='?', help='Assembly file to execute')
    
    args = parser.parse_args()
    
    # Get input file
    if args.file:
        asm_file = args.file
    else:
        asm_file = input("Enter RISC-V assembly file path: ").strip()
    
    # Create simulator
    sim = RISCVSimulator()
    
    # Load program
    if not sim.load_program(asm_file):
        print("ERROR: Failed to load program")
        return 1
    
    # Run program
    exit_code = sim.run()
    
    print(f"\nProgram exited with code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
