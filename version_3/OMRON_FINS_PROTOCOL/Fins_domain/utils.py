"""
FINS Domain Utilities
=====================
This module contains utility functions for FINS protocol operations.
"""

__version__ = "0.1.0"


def reverse_word_order(data: bytes) -> bytes:
    """
    Reverse word order in byte string.
    
    This function is helpful because FINS reads come in from low to high
    bytes, but since the data is represented as big-endian, the word order 
    of bytes needs to be reversed after reading and before writing data.
    
    Args:
        data: Input bytes to reverse word order
        
    Returns:
        Bytes with reversed word order
        
    Raises:
        ValueError: If data length is not even (incomplete words)
    """
    if len(data) % 2 != 0:
        raise ValueError("Data length must be even (complete words)")
    
    if len(data) == 0:
        return data
    
    reversed_bytes = data[::-1]
    reversed_words = b''
    
    for i in range(0, len(reversed_bytes), 2):
        reversed_words += reversed_bytes[i+1].to_bytes(1, 'big') + reversed_bytes[i].to_bytes(1, 'big')
    
    return reversed_words


def validate_address_format(address: bytes) -> bool:
    """
    Validate FINS address format.
    
    Args:
        address: Address bytes to validate
        
    Returns:
        True if valid format, False otherwise
    """
    return len(address) == 3


def format_address(word_address: int, bit_address: int = 0) -> bytes:
    """
    Format word and bit address into FINS address format.
    
    Args:
        word_address: Word address (0-65535)
        bit_address: Bit address (0-15)
        
    Returns:
        Formatted address as 3 bytes
        
    Raises:
        ValueError: If addresses are out of valid range
    """
    if not (0 <= word_address <= 65535):
        raise ValueError("Word address must be between 0 and 65535")
    
    if not (0 <= bit_address <= 15):
        raise ValueError("Bit address must be between 0 and 15")
    
    return word_address.to_bytes(2, 'big') + bit_address.to_bytes(1, 'big')


def parse_address(address: bytes) -> tuple:
    """
    Parse FINS address format into word and bit addresses.
    
    Args:
        address: 3-byte address
        
    Returns:
        Tuple of (word_address, bit_address)
        
    Raises:
        ValueError: If address format is invalid
    """
    if not validate_address_format(address):
        raise ValueError("Address must be exactly 3 bytes")
    
    word_address = int.from_bytes(address[:2], 'big')
    bit_address = int.from_bytes(address[2:3], 'big')
    
    return word_address, bit_address
