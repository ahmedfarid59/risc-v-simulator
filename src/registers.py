"""
RISC-V Register File Implementation
Manages 32 RISC-V registers with proper validation and logging
"""
from .constants import regsNames, NUM_REGISTERS, REGISTER_WIDTH
from .logger import logger


class RegisterError(Exception):
    """Custom exception for register-related errors"""
    pass


class registers(dict):
    """
    RISC-V register file with 32 registers (x0-x31)
    
    Features:
    - x0 is hardwired to zero (writes are ignored)
    - All registers are 32-bit
    - Supports both numbered (x0-x31) and ABI names (zero, ra, sp, etc.)
    """
    
    def __init__(self):
        """Initialize all 32 registers to zero"""
        super().__init__({key.upper(): 0 for key in regsNames.values()})
        logger.debug(f"Initialized {NUM_REGISTERS} registers")
    
    def _normalize_key(self, key):
        """
        Normalize register name to standard format
        
        Args:
            key: Register name (can be ABI name or x-notation)
        
        Returns:
            str: Normalized register name (X0-X31)
        
        Raises:
            RegisterError: If register name is invalid
        """
        if not isinstance(key, str):
            raise RegisterError(f"Register key must be string, got {type(key)}")
        
        # Try to lookup ABI name (lowercase), then convert result to uppercase
        key_lower = key.lower()
        if key_lower in regsNames:
            normalized = regsNames[key_lower].upper()  # Convert x17 -> X17
        else:
            normalized = key.upper()  # Already in X notation
        
        if normalized not in self:
            raise RegisterError(f"Invalid register name: {key}")
        
        return normalized
    
    def __setitem__(self, key, value):
        """
        Set register value with validation
        
        Args:
            key: Register name
            value: Value to set (will be masked to 32 bits)
        """
        try:
            normalized_key = self._normalize_key(key)
            
            # x0 is hardwired to zero
            if normalized_key == 'X0':
                logger.debug("Attempt to write to x0 ignored")
                return
            
            # Validate and mask value to 32 bits
            try:
                value = int(value) & 0xFFFFFFFF
            except (ValueError, TypeError) as e:
                raise RegisterError(f"Invalid register value: {value} - {e}")
            
            old_value = super().__getitem__(normalized_key)
            super().__setitem__(normalized_key, value)
            
            logger.debug(f"Register {normalized_key}: {old_value} -> {value} (0x{value:08X})")
            
        except RegisterError as e:
            logger.error(f"Register set error: {e}")
            raise
    
    def __getitem__(self, key):
        """
        Get register value
        
        Args:
            key: Register name
        
        Returns:
            int: Register value
        """
        try:
            normalized_key = self._normalize_key(key)
            value = super().__getitem__(normalized_key)
            logger.debug(f"Register {normalized_key} read: {value} (0x{value:08X})")
            return value
        except RegisterError as e:
            logger.error(f"Register get error: {e}")
            raise
    
    def get(self, key, default=None):
        """
        Get register value with default
        
        Args:
            key: Register name
            default: Default value if key not found
        
        Returns:
            int: Register value or default
        """
        try:
            normalized_key = self._normalize_key(key)
            return super().get(normalized_key, default)
        except RegisterError:
            return default
    
    def __delitem__(self, key):
        """Prevent register deletion"""
        logger.warning(f"Attempt to delete register {key} ignored")
        pass
    
    def __str__(self):
        """
        Format register file as readable string
        
        Returns:
            str: Formatted register dump
        """
        string = "-" * 80 + "\n"
        string += f"{'Register':<10} {'Decimal':<12} {'Hex':<12} {'Binary':<34}\n"
        string += "-" * 80 + "\n"
        
        for key, value in sorted(self.items()):
            # Handle negative values for display
            signed_value = value if value < 0x80000000 else value - 0x100000000
            string += f"{key:<10} {signed_value:<12} {hex(value):<12} {bin(value):<34}\n"
        
        string += "-" * 80
        return string
    
    def reset(self):
        """Reset all registers to zero"""
        for key in self.keys():
            if key != 'X0':
                super().__setitem__(key, 0)
        logger.info("All registers reset to zero")
    
    def dump(self):
        """
        Get register dump as dictionary
        
        Returns:
            dict: Copy of all register values
        """
        return dict(self)

