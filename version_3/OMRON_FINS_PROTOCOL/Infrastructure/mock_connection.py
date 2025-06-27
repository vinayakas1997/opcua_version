"""
FINS Mock Connection Implementation
===================================
This module provides a mock implementation for testing and development.
"""

import time
from typing import Dict, Any

from ...Fins_domain.connection import FinsConnection
from ...Fins_domain.frames import FinsResponseFrame, FinsCommandFrame
from ...Fins_domain.command_codes import FinsCommandCode
from ...Fins_domain.response_codes import FinsResponseEndCode

__version__ = "0.1.0"


class FinsMockConnection(FinsConnection):
    """
    Mock implementation of FINS protocol connection for testing.
    
    This class simulates PLC responses without requiring actual hardware.
    """
    
    def __init__(self, simulate_delay: bool = False, delay_ms: int = 10):
        """
        Initialize mock connection.
        
        Args:
            simulate_delay: Whether to simulate network delay
            delay_ms: Simulated delay in milliseconds
        """
        super().__init__()
        self.simulate_delay = simulate_delay
        self.delay_ms = delay_ms
        self.connected = True
        
        # Mock memory storage
        self.memory_storage: Dict[str, Dict[int, bytes]] = {
            'CIO_WORD': {},
            'WORK_WORD': {},
            'HOLDING_WORD': {},
            'DATA_MEMORY_WORD': {}
        }
        
        # Initialize with some test data
        self._initialize_test_data()
    
    def _initialize_test_data(self) -> None:
        """Initialize mock memory with test data."""
        # Add some sample data for testing
        self.memory_storage['WORK_WORD'][0] = b'\x12\x34'
        self.memory_storage['WORK_WORD'][1] = b'\x56\x78'
        self.memory_storage['CIO_WORD'][100] = b'\xAB\xCD'
        self.memory_storage['DATA_MEMORY_WORD'][0] = b'\xFF\xFF'
    
    def connect(self) -> None:
        """Mock connection - always succeeds."""
        self.connected = True
    
    def disconnect(self) -> None:
        """Mock disconnection."""
        self.connected = False
    
    def execute_fins_command_frame(self, fins_command_frame: bytes) -> bytes:
        """
        Execute a mock FINS command frame.
        
        Args:
            fins_command_frame: Complete FINS command frame
            
        Returns:
            Mock response frame bytes
        """
        if not self.connected:
            raise ConnectionError("Mock connection not established")
        
        if self.simulate_delay:
            time.sleep(self.delay_ms / 1000.0)
        
        # Parse command frame
        command_frame = FinsCommandFrame()
        command_frame.from_bytes(fins_command_frame)
        
        # Create response frame
        response_frame = FinsResponseFrame()
        response_frame.header = command_frame.header
        response_frame.command_code = command_frame.command_code
        response_frame.end_code = FinsResponseEndCode().NORMAL_COMPLETION
        
                # Handle different command types
        if command_frame.command_code == FinsCommandCode().MEMORY_AREA_READ:
            response_frame.text = self._handle_memory_read(command_frame.text)
        elif command_frame.command_code == FinsCommandCode().MEMORY_AREA_WRITE:
            response_frame.text = self._handle_memory_write(command_frame.text)
        elif command_frame.command_code == FinsCommandCode().CPU_UNIT_STATUS_READ:
            response_frame.text = self._handle_cpu_status_read()
        elif command_frame.command_code == FinsCommandCode().CPU_UNIT_DATA_READ:
            response_frame.text = self._handle_cpu_data_read()
        elif command_frame.command_code == FinsCommandCode().RUN:
            response_frame.text = b''  # No data for run command
        elif command_frame.command_code == FinsCommandCode().STOP:
            response_frame.text = b''  # No data for stop command
        else:
            # Unknown command - return error
            response_frame.end_code = FinsResponseEndCode().COMMAND_ERROR
            response_frame.text = b''
        
        return response_frame.bytes()
    
    def _handle_memory_read(self, command_data: bytes) -> bytes:
        """
        Handle mock memory area read command.
        
        Args:
            command_data: Command data containing memory area and address info
            
        Returns:
            Mock memory data
        """
        if len(command_data) < 6:
            return b''
        
        memory_area_code = command_data[0:1]
        word_address = int.from_bytes(command_data[1:3], 'big')
        bit_address = command_data[3]
        num_items = int.from_bytes(command_data[4:6], 'big')
        
        # Map memory area codes to storage keys
        area_mapping = {
            b'\xB0': 'CIO_WORD',
            b'\xB1': 'WORK_WORD', 
            b'\xB2': 'HOLDING_WORD',
            b'\x82': 'DATA_MEMORY_WORD'
        }
        
        storage_key = area_mapping.get(memory_area_code, 'WORK_WORD')
        storage = self.memory_storage[storage_key]
        
        # Generate mock data
        result_data = b''
        for i in range(num_items):
            addr = word_address + i
            if addr in storage:
                result_data += storage[addr]
            else:
                # Return zeros for uninitialized memory
                result_data += b'\x00\x00'
        
        return result_data
    
    def _handle_memory_write(self, command_data: bytes) -> bytes:
        """
        Handle mock memory area write command.
        
        Args:
            command_data: Command data containing memory area, address, and data
            
        Returns:
            Empty bytes (write commands don't return data)
        """
        if len(command_data) < 6:
            return b''
        
        memory_area_code = command_data[0:1]
        word_address = int.from_bytes(command_data[1:3], 'big')
        bit_address = command_data[3]
        num_items = int.from_bytes(command_data[4:6], 'big')
        write_data = command_data[6:]
        
        # Map memory area codes to storage keys
        area_mapping = {
            b'\xB0': 'CIO_WORD',
            b'\xB1': 'WORK_WORD',
            b'\xB2': 'HOLDING_WORD', 
            b'\x82': 'DATA_MEMORY_WORD'
        }
        
        storage_key = area_mapping.get(memory_area_code, 'WORK_WORD')
        storage = self.memory_storage[storage_key]
        
        # Store the data
        for i in range(num_items):
            addr = word_address + i
            data_start = i * 2
            data_end = data_start + 2
            if data_end <= len(write_data):
                storage[addr] = write_data[data_start:data_end]
        
        return b''  # Write commands return no data
    
    def _handle_cpu_status_read(self) -> bytes:
        """
        Handle mock CPU status read command.
        
        Returns:
            Mock CPU status data
        """
        # Mock CPU status: Running, no errors
        return b'\x00\x01\x00\x00\x00\x00'
    
    def _handle_cpu_data_read(self) -> bytes:
        """
        Handle mock CPU data read command.
        
        Returns:
            Mock CPU data
        """
        # Mock CPU data: Model, version, etc.
        return b'MOCK_PLC\x00\x01\x02\x03\x04\x05\x06\x07'
    
    def set_memory_value(self, area: str, address: int, value: bytes) -> None:
        """
        Set a value in mock memory for testing.
        
        Args:
            area: Memory area name
            address: Word address
            value: Value to set (2 bytes)
        """
        if area in self.memory_storage:
            self.memory_storage[area][address] = value
    
    def get_memory_value(self, area: str, address: int) -> bytes:
        """
        Get a value from mock memory for testing.
        
        Args:
            area: Memory area name
            address: Word address
            
        Returns:
            Value at address or zeros if not set
        """
        if area in self.memory_storage:
            return self.memory_storage[area].get(address, b'\x00\x00')
        return b'\x00\x00'
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

