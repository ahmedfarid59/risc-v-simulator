"""
Shared Utilities for RISC-V Simulator
Common functions and classes used across multiple modules
"""


class ParseError(Exception):
    """Custom exception for parsing errors"""
    pass


class ExecutionError(Exception):
    """Custom exception for instruction execution errors"""
    pass


class RegisterError(Exception):
    """Custom exception for register-related errors"""
    pass


class SimulatorError(Exception):
    """Custom exception for simulator errors"""
    pass


def print_banner(title, width=80):
    """
    Print a formatted banner
    
    Args:
        title: Banner title
        width: Width of banner (default 80)
    
    Returns:
        str: Formatted banner string
    """
    banner = "\n" + "="*width + "\n"
    banner += title + "\n"
    banner += "="*width
    return banner


def parse_immediate(value_str):
    """
    Parse immediate value (decimal, hex, or binary) - robust handling of noisy input
    
    Args:
        value_str: String representation of value
    
    Returns:
        int: Parsed value
        
    Raises:
        ValueError: If value cannot be parsed
    """
    try:
        # Convert to string and strip all whitespace
        value_str = str(value_str).strip()
        
        # Remove underscores (some assemblers allow 0x1_000)
        value_str = value_str.replace('_', '')
        
        # Handle empty string
        if not value_str:
            raise ValueError("Empty value string")
        
        # Hex (case-insensitive)
        if value_str.lower().startswith('0x'):
            return int(value_str, 16)
        
        # Binary
        if value_str.lower().startswith('0b'):
            return int(value_str, 2)
        
        # Octal (leading 0)
        if value_str.startswith('0') and len(value_str) > 1 and value_str[1].isdigit():
            return int(value_str, 8)
        
        # Decimal (can be negative)
        return int(value_str)
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot parse immediate value '{value_str}': {e}")


def normalize_register(reg_str):
    """
    Normalize register name - handles various formats and extra whitespace
    
    Args:
        reg_str: Register string (e.g., 'x1', 'X1', ' x1 ', 'a0')
    
    Returns:
        str: Normalized uppercase register name
    """
    reg_str = str(reg_str).strip().upper()
    return reg_str


def sign_extend(value, bits):
    """
    Sign-extend a value to 32 bits
    
    Args:
        value: Value to extend (can be int or string with hex/binary/decimal)
        bits: Number of bits in the original value
    
    Returns:
        int: Sign-extended 32-bit value
    """
    try:
        # Parse the value if it's a string (handles hex, binary, decimal)
        if isinstance(value, str):
            value = parse_immediate(value)
        else:
            value = int(value)
            
        sign_bit = 1 << (bits - 1)
        mask = (1 << bits) - 1
        value = value & mask
        
        if value & sign_bit:
            # Negative number - extend with 1s
            result = value | (~mask & 0xFFFFFFFF)
        else:
            # Positive number - already correct
            result = value
        
        return result if result < 0x80000000 else result - 0x100000000
        
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid value for sign extension: {value}: {e}")
