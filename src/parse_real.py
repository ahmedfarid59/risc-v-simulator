"""
Real-World RISC-V Assembly Parser
Simplified parser for the real-world simulator with proper memory management
"""
import re
from .logger import logger
from .constants import *
from .utils import ParseError, parse_immediate


def parse_program(file_path, memory):
    """
    Parse RISC-V assembly program for real-world simulator
    
    Args:
        file_path: Path to assembly file
        memory: Memory instance to load data into
    
    Returns:
        tuple: (success, instructions, labels, data_bytes, vars_map)
    """
    try:
        logger.info(f"Parsing program: {file_path}")
        
        # Read file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        instructions = []
        labels = {}
        vars_map = {}
        data_bytes = bytearray()
        
        current_section = None
        data_offset = 0
        instruction_index = 0
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments (handle both # and ; style)
            if '#' in line:
                line = line[:line.index('#')]
            if ';' in line:
                line = line[:line.index(';')]
            
            # Replace tabs with spaces
            line = line.replace('\t', ' ')
            
            # Strip all leading/trailing whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for section directives (case-insensitive)
            if line.lower().startswith('.'):
                directive = line.lower().strip()
                if directive == '.text':
                    current_section = 'text'
                    logger.debug("Entered .text section")
                    continue
                elif directive == '.data':
                    current_section = 'data'
                    logger.debug("Entered .data section")
                    continue
            
            # Process based on current section
            if current_section == 'data':
                # Parse data directives
                result = parse_data_line(line, data_offset, vars_map)
                if result:
                    data_bytes.extend(result['bytes'])
                    data_offset += len(result['bytes'])
                    
            elif current_section == 'text':
                # Check for label (handle extra spaces around colon)
                if ':' in line:
                    # Split on colon to handle labels
                    colon_idx = line.index(':')
                    label_part = line[:colon_idx].strip()
                    rest = line[colon_idx+1:].strip()
                    
                    if label_part:
                        labels[label_part.upper()] = instruction_index
                        logger.debug(f"Label '{label_part}' at instruction {instruction_index}")
                    
                    # If there's instruction after label, process it
                    if rest:
                        line = rest
                    else:
                        continue
                
                # Parse instruction - handle multiple spaces, tabs, commas
                # First normalize: replace tabs and multiple spaces with single space
                line = re.sub(r'\s+', ' ', line)
                # Convert parentheses format to comma format: offset(reg) -> offset,reg
                line = re.sub(r'\s*\(\s*', ',', line)
                line = re.sub(r'\s*\)', '', line)
                # Split on both commas and spaces
                parts = re.split(r'[,\s]+', line)
                parts = [p.strip() for p in parts if p.strip()]
                
                if parts:
                    instructions.append(parts)
                    instruction_index += 1
        
        # Load data into memory
        if data_bytes:
            logger.info(f"Loading {len(data_bytes)} bytes of data at 0x{DATA_START:08X}")
            memory.write_bytes(DATA_START, bytes(data_bytes))
        
        logger.info(f"Parsed {len(instructions)} instructions, {len(labels)} labels, {len(vars_map)} variables")
        return True, instructions, labels, data_bytes, vars_map
        
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return False, [], {}, bytearray(), {}
    except Exception as e:
        logger.error(f"Parse error: {e}")
        return False, [], {}, bytearray(), {}


def parse_data_line(line, offset, vars_map):
    """
    Parse a data directive line - handles noisy input with extra spaces
    
    Args:
        line: Line to parse
        offset: Current data offset
        vars_map: Dictionary to store variable mappings
    
    Returns:
        dict: {'bytes': bytearray, 'size': int} or None
    """
    try:
        # Normalize line: replace multiple spaces/tabs with single space
        line = re.sub(r'\s+', ' ', line)
        
        # Match: label: .directive value (with flexible spacing)
        # Handle optional spaces around colon and after directive
        match = re.match(r'(\w+)\s*:\s*\.(\w+)\s+(.+)', line, re.IGNORECASE)
        if not match:
            return None
        
        var_name = match.group(1).upper()
        directive = match.group(2).lower()
        value_str = match.group(3).strip()
        
        data = bytearray()
        
        if directive == 'word':
            # .word - 4 bytes (can be single value or array)
            # Handle arrays: .word 1, 2, 3, 4, 5
            if ',' in value_str:
                # Array of values
                values = [v.strip() for v in value_str.split(',')]
                for val_str in values:
                    value = parse_immediate(val_str)
                    data.extend(value.to_bytes(4, byteorder='big', signed=True))
                vars_map[var_name] = {'addr': DATA_START + offset, 'size': len(data), 'type': 'word'}
            else:
                # Single value
                value = parse_immediate(value_str)
                data = value.to_bytes(4, byteorder='big', signed=True)
                vars_map[var_name] = {'addr': DATA_START + offset, 'size': 4, 'type': 'word'}
            
        elif directive == 'half':
            # .half - 2 bytes
            value = parse_immediate(value_str)
            data = value.to_bytes(2, byteorder='big', signed=True)
            vars_map[var_name] = {'addr': DATA_START + offset, 'size': 2, 'type': 'half'}
            
        elif directive == 'byte':
            # .byte - 1 byte
            value = parse_immediate(value_str)
            data = value.to_bytes(1, byteorder='big', signed=True)
            vars_map[var_name] = {'addr': DATA_START + offset, 'size': 1, 'type': 'byte'}
            
        elif directive == 'ascii' or directive == 'asciz':
            # String (asciz adds null terminator)
            # Handle various quote styles: "string", 'string', or string
            string = value_str.strip()
            # Remove quotes (both single and double)
            if (string.startswith('"') and string.endswith('"')) or \
               (string.startswith("'") and string.endswith("'")):
                string = string[1:-1]
            data = bytearray(string.encode('utf-8'))
            if directive == 'asciz':
                data.append(0)  # Null terminator
            vars_map[var_name] = {'addr': DATA_START + offset, 'size': len(data), 'type': directive}
            
        elif directive == 'space':
            # Reserve space
            size = parse_immediate(value_str)
            data = bytearray(size)
            vars_map[var_name] = {'addr': DATA_START + offset, 'size': size, 'type': 'space'}
        
        else:
            logger.warning(f"Unknown directive: .{directive}")
            return None
        
        logger.debug(f"Variable '{var_name}' at offset {offset}, size {len(data)}, type .{directive}")
        return {'bytes': data, 'size': len(data)}
        
    except Exception as e:
        logger.error(f"Error parsing data line '{line}': {e}")
        return None


def clean_assembly(file_path):
    """
    Clean and normalize assembly file - robust handling of noisy input
    
    Args:
        file_path: Path to assembly file
    
    Returns:
        list: List of cleaned lines
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        cleaned = []
        for line in lines:
            # Remove comments (handle both # and ; styles)
            if '#' in line:
                line = line[:line.index('#')]
            if ';' in line:
                line = line[:line.index(';')]
            
            # Replace tabs with spaces
            line = line.replace('\t', ' ')
            
            # Strip all leading/trailing whitespace
            line = line.strip()
            
            # Remove multiple consecutive spaces
            line = re.sub(r' {2,}', ' ', line)
            
            # Skip empty lines
            if line:
                cleaned.append(line)
        
        return cleaned
        
    except Exception as e:
        logger.error(f"Error cleaning assembly: {e}")
        return []
