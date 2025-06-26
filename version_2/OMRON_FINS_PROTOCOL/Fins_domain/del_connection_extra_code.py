"""
FINS Connection Interface
=========================
This module defines the abstract interface for FINS protocol connections.
"""

import struct
import time
from abc import ABCMeta, abstractmethod
from typing import List, Union, Any

from .command_codes import FinsCommandCode
from .frames import FinsResponseFrame
from .memory_areas import FinsPLCMemoryAreas
from .utils import reverse_word_order, format_address

__version__ = "0.1.0"


class FinsConnection(metaclass=ABCMeta):
    """
    Abstract base class for FINS protocol connections.
    
    This class defines the interface that all FINS connection implementations
    must follow, regardless of the underlying transport (TCP, UDP, Serial).
    """
    
    def __init__(self):
        """Initialize connection parameters."""
        self.dest_node_add = 0
        self.srce_node_add = 0
        self.dest_net_add = 0
        self.srce_net_add = 0
        self.dest_unit_add = 0
        self.srce_unit_add = 0
    
    @abstractmethod
    def execute_fins_command_frame(self, fins_command_frame: bytes) -> bytes:
        """
        Execute a FINS command frame and return the response.
        
        Args:
            fins_command_frame: Complete FINS command frame as bytes
            
        Returns:
            Response frame as bytes
            
        Raises:
            ConnectionError: If communication fails
        """
        pass
    
    def fins_command_frame(self, command_code: bytes, text: bytes = b'', 
                          service_id: bytes = b'\x60', icf: bytes = b'\x80', 
                          gct: bytes = b'\x07', rsv: bytes = b'\x00') -> bytes:
        """
        Build a complete FINS command frame.
        
        Args:
            command_code: FINS command code
            text: Command data payload
            service_id: Service identifier
            icf: Information Control Field
            gct: Gateway Count
            rsv: Reserved field
            
        Returns:
            Complete command frame as bytes
        """
        command_bytes = (icf + rsv + gct +
                        self.dest_net_add.to_bytes(1, 'big') + 
                        self.dest_node_add.to_bytes(1, 'big') +
                        self.dest_unit_add.to_bytes(1, 'big') + 
                        self.srce_net_add.to_bytes(1, 'big') +
                        self.srce_node_add.to_bytes(1, 'big') + 
                        self.srce_unit_add.to_bytes(1, 'big') +
                        service_id + command_code + text)
        return command_bytes
    
    def get_values(self, _format: str, read_area: bytes, begin_address: bytes,
                   words_per_value: int, number_of_values: int = 1) -> Union[Any, List[Any]]:
        """
        Read and parse values from PLC memory.
        
        Args:
            _format: Struct format string for unpacking
            read_area: Memory area code
            begin_address: Starting address (3 bytes)
            words_per_value: Number of words per value
            number_of_values: Number of values to read
            
        Returns:
            Single value or list of values
        """
        fins_response = FinsResponseFrame()
        number_of_words = number_of_values * words_per_value
        response = self.memory_area_read(read_area, begin_address, number_of_words)
        fins_response.from_bytes(response)
        data = fins_response.text
        bytes_per_value = words_per_value * 2
        
        if number_of_values > 1:
            value = []
            for i in range(number_of_values):
                value_data = data[i * bytes_per_value: i * bytes_per_value + bytes_per_value]
                value_data = reverse_word_order(value_data)
                single_value = struct.unpack(_format, value_data)[0]
                value.append(single_value)
        else:
            data = reverse_word_order(data)
            value = struct.unpack(_format, data)[0]
        return value
    
    def set_values(self, _format: str, read_area: bytes, begin_address: bytes,
                   words_per_value: int, value: Union[Any, List[Any]]) -> FinsResponseFrame:
        """
        Write values to PLC memory.
        
        Args:
            _format: Struct format string for packing
            read_area: Memory area code
            begin_address: Starting address (3 bytes)
            words_per_value: Number of words per value
            value: Single value or list of values to write
            
        Returns:
            FINS response frame
        """
        fins_response = FinsResponseFrame()
        if isinstance(value, list):
            number_of_values = len(value)
        else:
            number_of_values = 1
        
        number_of_words = number_of_values * words_per_value
        bytes_per_value = words_per_value * 2
        
        if number_of_values > 1:
            value_data = b''
            for i in range(number_of_values):
                single_value_data = struct.pack(_format, value[i])
                single_value_data = reverse_word_order(single_value_data)
                value_data += single_value_data
            data = value_data
        else:
            data = struct.pack(_format, value)
            data = reverse_word_order(data)
        
        response = self.memory_area_write(read_area, begin_address, data, number_of_words)
        fins_response.from_bytes(response)
        return fins_response
    
    def read(self, memory_area: str, word_address: int,
             data_type: str = 'w', number_of_values: int = 1) -> Union[Any, List[Any]]:
        """
        High-level read operation with data type conversion.
        
        Data Types:
        - b: BOOL (bit)
        - ui: UINT (one-word unsigned binary)
        - udi: UDINT (two-word unsigned binary)  
        - uli: ULINT (four-word unsigned binary)
        - i: INT (one-word signed binary)
        - d: DINT (two-word signed binary)
        - l: LINT (four-word signed binary)
        - r: REAL (two-word floating point)
        - lr: LREAL (four-word floating point)
        - w: WORD (one-word hexadecimal)
        - dw: DWORD (two-word hexadecimal)
        - lw: LWORD (four-word hexadecimal)
        
        Memory Areas:
        - w: work area
        - c: cio area  
        - d: data memory
        - h: holding
        
        Args:
            memory_area: Memory area identifier
            word_address: Word address to read from
            data_type: Data type for interpretation
            number_of_values: Number of values to read
            
        Returns:
            Read value(s) with appropriate type conversion
        """
        fins_memory_area_instance = FinsPLCMemoryAreas()
        bit_address = 0
        begin_address = format_address(word_address, bit_address)
        
        # Map memory area characters to memory area codes
        area_mapping = {
            'w': fins_memory_area_instance.WORK_WORD,
            'c': fins_memory_area_instance.CIO_WORD,
            'd': fins_memory_area_instance.DATA_MEMORY_WORD,
            'h': fins_memory_area_instance.HOLDING_WORD
        }
        
        read_area = area_mapping.get(memory_area)
        if read_area is None:
            raise ValueError(f"Unknown memory area: {memory_area}")
        
        # Map data types to format strings and word counts
        type_mapping = {
            'r': ('>f', 2),    # Real (float)
            'lr': ('>d', 4),   # Long Real (double)
            'i': ('>h', 1),    # Signed int
            'di': ('>i', 2),   # Double int
            'li': ('>q', 4),   # Long int
            'ui': ('>H', 1),   # Unsigned int
            'udi': ('>I', 2),  # Unsigned double int
            'uli': ('>Q', 4),  # Unsigned long int
            'w': ('2s', 1),    # Word as bytes
            'dw': ('4s', 2),   # Double word as bytes
            'lw': ('8s', 4),   # Long word as bytes
        }
        
        format_info = type_mapping.get(data_type)
        if format_info is None:
            raise ValueError(f"Unknown data type: {data_type}")
        
        format_str, words_per_value = format_info
        return self.get_values(format_str, read_area, begin_address, words_per_value, number_of_values)
    
    def write(self, value: Union[Any, List[Any]], memory_area: str, word_address: int,
              data_type: str = 'w') -> FinsResponseFrame:
        """
        High-level write operation with data type conversion.
        
        Args:
            value: Value(s) to write
            memory_area: Memory area identifier  
            word_address: Word address to write to
            data_type: Data type for conversion
            
        Returns:
            FINS response frame
        """
        fins_memory_area_instance = FinsPLCMemoryAreas()
        bit_address = 0
        begin_address = format_address(word_address, bit_address)
        
        # Map memory area characters to memory area codes
        area_mapping = {
            'w': fins_memory_area_instance.WORK_WORD,
            'c': fins_memory_area_instance.CIO_WORD,
            'd': fins_memory_area_instance.DATA_MEMORY_WORD,
            'h': fins_memory_area_instance.HOLDING_WORD
        }
        
        read_area = area_mapping.get(memory_area)
        if read_area is None:
            raise ValueError(f"Unknown memory area: {memory_area}")
        
        # Map data types to format strings and word counts
        type_mapping = {
            'r': ('>f', 2),    # Real (float)
            'lr': ('>d', 4),   # Long Real (double)
            'i': ('>h', 1),    # Signed int
            'di': ('>i', 2),   # Double int
            'li': ('>q', 4),   # Long int
            'ui': ('>H', 1),   # Unsigned int
            'udi': ('>I', 2),  # Unsigned double int
            'uli': ('>Q', 4),  # Unsigned long int
            'w': ('2s', 1),    # Word as bytes
            'dw': ('4s', 2),   # Double word as bytes
            'lw': ('8s', 4),   # Long word as bytes
        }
        
        format_info = type_mapping.get(data_type)
        if format_info is None:
            raise ValueError(f"Unknown data type: {data_type}")
        
        format_str, words_per_value = format_info
        return self.set_values(format_str, read_area, begin_address, words_per_value, value)
    
    # Low-level FINS command methods
    def memory_area_read(self, memory_area_code: bytes, beginning_address: bytes = b'\x00\x00\x00', 
                        number_of_items: int = 1) -> bytes:
        """
        Read PLC memory areas.
        
        Args:
            memory_area_code: Memory area to read
            beginning_address: Beginning address (3 bytes)
            number_of_items: Number of items to read
            
        Returns:
            Raw response bytes
        """
        if len(beginning_address) != 3:
            raise ValueError("Beginning address must be exactly 3 bytes")
        
        data = memory_area_code + beginning_address + number_of_items.to_bytes(2, 'big')
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().MEMORY_AREA_READ, data))
        return response
    
    def memory_area_write(self, memory_area_code: bytes, beginning_address: bytes = b'\x00\x00\x00',
                         write_bytes: bytes = b'', number_of_items: int = 0) -> bytes:
        """
        Write PLC memory areas.
        
        Args:
            memory_area_code: Memory area to write
            beginning_address: Beginning address (3 bytes)
            write_bytes: The bytes to write
            number_of_items: The number of words
            
        Returns:
            Raw response bytes
        """
        if len(beginning_address) != 3:
            raise ValueError("Beginning address must be exactly 3 bytes")
        
        data = memory_area_code + beginning_address + number_of_items.to_bytes(2, 'big') + write_bytes
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().MEMORY_AREA_WRITE, data))
        return response
    
    def program_area_read(self, beginning_word: int, number_of_bytes: int = 992) -> bytes:
        """
        Read PLC program area.
        
        Args:
            beginning_word: Word to start read
            number_of_bytes: Number of bytes to read
            
        Returns:
            Raw response bytes
        """
        program_number = b'\xff\xff'
        data = program_number + beginning_word.to_bytes(4, 'big') + number_of_bytes.to_bytes(2, 'big')
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().PROGRAM_AREA_READ, data))
        return response
    
    def program_area_write(self, beginning_word: int, number_of_bytes: int, program_data: bytes) -> bytes:
        """
        Write data to PLC program area.
        
        Args:
            beginning_word: Word to start write
            number_of_bytes: Number of bytes to write
            program_data: Program data to write
            
        Returns:
            Raw response bytes
        """
        program_number = b'\xff\xff'
        data = program_number + beginning_word.to_bytes(4, 'big') + number_of_bytes.to_bytes(2, 'big') + program_data
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().PROGRAM_AREA_WRITE, data))
        return response
    
    def cpu_unit_data_read(self, data: bytes = b'') -> bytes:
        """
        Read CPU unit data.
        
        Args:
            data: Additional data for the command
            
        Returns:
            Raw response bytes
        """
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().CPU_UNIT_DATA_READ, data))
        return response
    
    def cpu_unit_status_read(self) -> bytes:
        """
        Read CPU unit status.
        
        Returns:
            Raw response bytes
        """
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().CPU_UNIT_STATUS_READ))
        return response
    
    def change_to_run_mode(self) -> bytes:
        """
        Change PLC to run mode.
        
        Returns:
            Raw response bytes
        """
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().RUN))
        return response
    
    def change_to_program_mode(self) -> bytes:
        """
        Change PLC to program mode.
        
        Returns:
            Raw response bytes
        """
        response = self.execute_fins_command_frame(
            self.fins_command_frame(FinsCommandCode().STOP))
        return response
    
    # High-level utility methods
    def plc_program_to_file(self, filename: str, number_of_read_bytes: int = 400) -> None:
        """
        Read the program from the connected FINS device and save to file.
        
        Args:
            filename: Filename to write the program to
            number_of_read_bytes: Bytes to read from the device per cycle
        """
        program_buffer = b''
        done = False
        current_word = 0
        
        with open(filename, 'wb') as output_file:
            while not done:
                response = self.program_area_read(current_word, number_of_read_bytes)
                # Strip FINS frame headers from response
                response = response[10:]
                # The MSB of the 10th Byte of response is the last word of data flag
                done = response[10] >= 0x80
                # Strip command information from response leaving only program data
                response = response[12:]
                program_buffer += response
                current_word += number_of_read_bytes
            
            output_file.write(program_buffer)
    
    def file_to_plc_program(self, filename: str, number_of_write_bytes: int = 400) -> None:
        """
        Write a stored hex program to the connected FINS device.
        
        Args:
            filename: Filename to read the program from
            number_of_write_bytes: Bytes to write per cycle
        """
        with open(filename, 'rb') as input_file:
            program_buffer = input_file.read()
        
        if len(program_buffer) % number_of_write_bytes != 0:
            write_cycles = len(program_buffer) // number_of_write_bytes + 1
        else:
            write_cycles = len(program_buffer) // number_of_write_bytes
        
        current_word = 0
        
        # PLC must be in program mode to do a program area write
        self.change_to_program_mode()
        
        try:
            for i in range(write_cycles):
                number_of_write_bytes_with_completion_flag = number_of_write_bytes
                if i == write_cycles - 1:
                    number_of_write_bytes = len(program_buffer) % number_of_write_bytes
                    number_of_write_bytes_with_completion_flag = number_of_write_bytes + 0x8000
                
                current_data = program_buffer[current_word:current_word + number_of_write_bytes]
                self.program_area_write(current_word, number_of_write_bytes_with_completion_flag, current_data)
                current_word += number_of_write_bytes
        finally:
            # Change back to run mode after PLC program is written
            self.change_to_run_mode()

