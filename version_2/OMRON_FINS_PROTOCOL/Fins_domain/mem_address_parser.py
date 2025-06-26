"""
FINS Address Parser
==================
This module handles parsing of PLC addresses and converts them to FINS protocol format.
"""

from OMRON_FINS_PROTOCOL.Fins_domain.memory_areas import FinsPLCMemoryAreas

__version__ = "0.1.0"


class FinsAddressParser:
    """
    Parser for PLC addresses in string format (e.g., 'D1000', 'W100', 'H200').
    Converts them to FINS protocol memory area codes and offsets.
    """
    
    def __init__(self):
        self.memory_areas = FinsPLCMemoryAreas()
    
    def parse(self, address: str, offset: int = 0) -> dict:
        """
        Main entry point - automatically detects if address is word or bit based on '.' presence.
        
        Args:
            address: Address string (e.g., 'A100' for word, 'A100.01' for bit)
            offset: Additional offset to add to the address
            
        Returns:
            Dictionary containing parsed address information
        """
        if not address:
            raise ValueError("Address cannot be empty")
        
        # Check if it's a bit address (contains '.')
        if '.' in address:
            return self._parse_as_bit_address(address, offset)
        else:
            return self._parse_as_word_address(address, offset)
    
    def _parse_as_bit_address(self, address: str, offset: int = 0) -> dict:
        """
        Parse as bit address (e.g., 'A100.01').
        
        Args:
            address: Bit address string
            offset: Additional offset to add to the word address
            
        Returns:
            Dictionary with bit address information
        """
        memory_type, moffset, bit_num = self.parse_bit_address(address, offset)
        
        # Convert memory type bytes to int if needed
        if isinstance(memory_type, bytes):
            memory_type_int = int.from_bytes(memory_type, 'big')
        else:
            memory_type_int = memory_type
        
        word_address = int.from_bytes(bytes(moffset), 'big')
        
        return {
            'address_type': 'bit',
            'original_address': address,
            'memory_area': self._get_memory_area_name(address),
            'memory_type_code': memory_type_int,
            'memory_type_bytes': memory_type,
            'word_address': word_address,
            'bit_number': bit_num,
            'offset_bytes': moffset,
            'fins_format': {
                'memory_area_code': memory_type,
                'address_high': moffset[0],
                'address_low': moffset[1],
                'bit_position': bit_num
            }
        }
    
    def _parse_as_word_address(self, address: str, offset: int = 0) -> dict:
        """
        Parse as word address (e.g., 'A100').
        
        Args:
            address: Word address string
            offset: Additional offset to add to the address
            
        Returns:
            Dictionary with word address information
        """
        memory_type, moffset = self.parse_address(address, offset)
        
        # Convert memory type bytes to int if needed
        if isinstance(memory_type, bytes):
            memory_type_int = int.from_bytes(memory_type, 'big')
        else:
            memory_type_int = memory_type
        
        word_address = int.from_bytes(bytes(moffset), 'big')
        
        return {
            'address_type': 'word',
            'original_address': address,
            'memory_area': self._get_memory_area_name(address),
            'memory_type_code': memory_type_int,
            'memory_type_bytes': memory_type,
            'word_address': word_address,
            'bit_number': None,
            'offset_bytes': moffset,
            'fins_format': {
                'memory_area_code': memory_type,
                'address_high': moffset[0],
                'address_low': moffset[1]
            }
        }

    def parse_address(self, address: str, offset: int = 0) -> tuple:
        """
        Parse a PLC address string and return memory type and offset.
        
        Args:
            address: Address string (e.g., 'D1000', 'W100', 'H200')
            offset: Additional offset to add to the address
            
        Returns:
            Tuple of (memory_type_code, offset_bytes_list)
        """
        if not address:
            raise ValueError("Address cannot be empty")
            
        mtype = address[:1].upper()
        moffset = []
        
        if mtype == 'D':  # Data Memory
            memory_type = self.memory_areas.DATA_MEMORY_WORD
            # addr_num = int(address[1:]) + offset
            # moffset = list(addr_num.to_bytes(2, 'big'))
            moffset = list((int(address[1:])+offset).to_bytes(2,'big'))
        elif mtype == 'E':  # Extended Memory
            if len(address) < 4:
                raise ValueError(f"Invalid extended memory address format: {address}")
            bank = int(address[1:2], 16)
            # Map to appropriate EM bank (EM0-EMF)
            if 0 <= bank <= 9:
                memory_type = getattr(self.memory_areas, f'EM{bank}_WORD')
            elif 10 <= bank <= 15:  # A=10, B=11, C=12, D=13, E=14, F=15
                bank_char = chr(ord('A') + bank - 10)
                memory_type = getattr(self.memory_areas, f'EM{bank_char}_WORD')
            else:
                raise ValueError(f"Invalid extended memory bank: {bank}")
            addr_num = int(address[3:]) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype.isdigit():  # CIO Area (numeric addresses)
            memory_type = self.memory_areas.CIO_WORD
            addr_num = int(address) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype == 'W':  # Work Area
            memory_type = self.memory_areas.WORK_WORD
            addr_num = int(address[1:]) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype == 'H':  # Holding Area
            memory_type = self.memory_areas.HOLDING_WORD
            addr_num = int(address[1:]) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype == 'A':  # Auxiliary Area
            memory_type = self.memory_areas.AUXILIARY_WORD
            addr_num = int(address[1:]) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype == 'T':  # Timer
            memory_type = self.memory_areas.TIMER_WORD
            addr_num = int(address[1:]) + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        elif mtype == 'C':  # Counter
            memory_type = self.memory_areas.COUNTER_WORD
            # Add counter offset as in your original code
            addr_num = int(address[1:]) + 0x0800 + offset
            moffset = list(addr_num.to_bytes(2, 'big'))
            
        else:
            raise ValueError(f"Unsupported memory type: {mtype}")
        
        return memory_type, moffset
    
    def parse_bit_address(self, address: str, offset: int = 0, bit: int = 0) -> tuple:
        """
        Parse a PLC bit address string with enhanced bit management.
        
        Args:
            address: Address string (e.g., 'A0.01', 'D1000.05', 'W100.15', '100.03')
            offset: Additional offset to add to the word address
            bit: Bit number (0-15) if not specified in address
            
        Returns:
            Tuple of (memory_type_code, offset_bytes_list, bit_number)
        """
        # Handle bit notation (e.g., 'A0.01', 'W100.05')
        if '.' in address:
            base_addr, bit_str = address.split('.')
            bit_num = int(bit_str)
        else:
            base_addr = address
            bit_num = bit if bit is not None else 0
            
        if not (0 <= bit_num <= 15):
            raise ValueError(f"Bit number must be between 0-15, got: {bit_num}")
        
        mtype = base_addr[:1].upper()
        
        if mtype == 'D':  # Data Memory
            memory_type = self.memory_areas.DATA_MEMORY_BIT
            addr_num = int(base_addr[1:]) + offset
            
        elif mtype == 'W':  # Work Area
            memory_type = self.memory_areas.WORK_BIT
            addr_num = int(base_addr[1:]) + offset
            
        elif mtype == 'H':  # Holding Area
            memory_type = self.memory_areas.HOLDING_BIT
            addr_num = int(base_addr[1:]) + offset
            
        elif mtype == 'A':  # Auxiliary Area
            memory_type = self.memory_areas.AUXILIARY_BIT
            addr_num = int(base_addr[1:]) + offset
            
        elif mtype == 'E':  # Extended Memory Bit
            if len(base_addr) < 4:
                raise ValueError(f"Invalid extended memory bit address format: {base_addr}")
            bank = int(base_addr[1:2], 16)
            # Map to appropriate EM bank bit areas
            if 0 <= bank <= 9:
                memory_type = getattr(self.memory_areas, f'EM{bank}_BIT')
            elif 10 <= bank <= 15:  # A=10, B=11, C=12, D=13, E=14, F=15
                bank_char = chr(ord('A') + bank - 10)
                memory_type = getattr(self.memory_areas, f'EM{bank_char}_BIT')
            else:
                raise ValueError(f"Invalid extended memory bank for bit access: {bank}")
            addr_num = int(base_addr[3:]) + offset
            
        # elif mtype == 'T':  # Timer Bit
        #     memory_type = self.memory_areas.TIMER_BIT
        #     addr_num = int(base_addr[1:]) + offset
            
        # elif mtype == 'C':  # Counter Bit
        #     memory_type = self.memory_areas.COUNTER_BIT
        #     addr_num = int(base_addr[1:]) + offset
            
        elif mtype.isdigit():  # CIO Area
            memory_type = self.memory_areas.CIO_BIT
            addr_num = int(base_addr) + offset
            
        else:
            raise ValueError(f"Unsupported bit memory type: {mtype}")
        
        moffset = list(addr_num.to_bytes(2, 'big'))
        return memory_type, moffset, bit_num

    def _get_memory_area_name(self, address: str) -> str:
        """
        Get human-readable memory area name from address.
        
        Args:
            address: Address string
            
        Returns:
            Memory area name
        """
        mtype = address[:1].upper()
        
        area_names = {
            'D': 'Data Memory',
            'W': 'Work Area',
            'H': 'Holding Area',
            'A': 'Auxiliary Area',
            'E': 'Extended Memory',
            'T': 'Timer',
            'C': 'Counter'
        }
        
        if mtype.isdigit():
            return 'CIO Area'
        
        return area_names.get(mtype, f'Unknown ({mtype})')

    def is_bit_address(self, address: str) -> bool:
        """
        Check if address is a bit address (contains '.').
        
        Args:
            address: Address string
            
        Returns:
            True if bit address, False if word address
        """
        return '.' in address

    def validate_address(self, address: str) -> bool:
        """
        Validate if an address is properly formatted.
        
        Args:
            address: Address string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self.parse(address)
            return True
        except (ValueError, AttributeError):
            return False


# class FinsAddressHelper:
#     """
#     Helper class that combines address parsing with your existing FINS class structure.
#     """
    
#     def __init__(self):
#         self.parser = FinsAddressParser()
    
#     def parse_any_address(self, address: str, offset: int = 0) -> dict:
#         """
#         Main entry point - parse any address (word or bit) automatically.
        
#         Args:
#             address: Address string (e.g., 'A100' or 'A100.01')
#             offset: Offset to add to the address
            
#         Returns:
#             Dictionary with parsed address information
#         """
#         return self.parser.parse(address, offset)
    
#     def offset(self, address: str, offset: int = 0) -> tuple:
#         """
#         Compatibility method that matches your existing offset method signature.
        
#         Args:
#             address: Address string (e.g., 'D1000', 'W100')
#             offset: Offset to add to the address
            
#         Returns:
#             Tuple of (memory_type_int, offset_bytes_list)
#         """
#         memory_type_bytes, moffset = self.parser.parse_address(address, offset)
#         # Convert bytes to int for compatibility with your existing code
#         memory_type_int = int.from_bytes(memory_type_bytes, 'big')
#         return memory_type_int, moffset


# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced address parser with automatic detection
    parser = FinsAddressParser()
    # helper = FinsAddressHelper()
    
    test_addresses = [
        # 'A100',      # Word address
        # 'A100.01',   # Bit address
        # 'D1000',     # Word address
        # 'D1000.05',  # Bit address
        # 'W200',      # Word address
        # 'W200.15',   # Bit address
        # '100',       # CIO word address
        # '100.03'     # CIO bit address
        'D0100'
    ]
    
    print("Testing automatic address detection:")
    print("=" * 50)
    
    for addr in test_addresses:
        try:
            info = parser.parse(addr)
            print(f"Address: {addr}")
            print(f"  Type: {info['address_type']}")
            print(f"  Memory Area: {info['memory_area']}")
            print(f"  Word Address: {info['word_address']}")
            if info['address_type'] == 'bit':
                print(f"  Bit Number: {info['bit_number']}")
            # print(f"  Memory Type Code: 0x{info['memory_type_code']:04X}")
            print(f"  Memory Type Code: {info['memory_type_code']}")
            print(f"  Offset Bytes: {info['offset_bytes']}")
            print()
        except Exception as e:
            print(f"Error parsing {addr}: {e}")
            print()
    
    # # Test helper class
    # print("\nTesting helper class:")
    # print("=" * 30)
    
    # for addr in ['A100', 'A100.01']:
    #     try:
    #         info = helper.parse_any_address(addr)
    #         print(f"Helper parsed {addr}:")
    #         print(f"  Type: {info['address_type']}")
    #         print(f"  Area: {info['memory_area']}")
    #         if info['bit_number'] is not None:
    #             print(f"  Bit: {info['bit_number']}")
    #         print()
    #     except Exception as e:
    #         print(f"Helper error with {addr}: {e}")