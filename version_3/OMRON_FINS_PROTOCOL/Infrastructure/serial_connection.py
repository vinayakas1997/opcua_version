"""
FINS Serial Connection Implementation
=====================================
This module provides serial communication implementation for FINS protocol.
"""

import serial
import time
from typing import Optional

from ...Fins_domain.connection import FinsConnection

__version__ = "0.1.0"


class FinsSerialConnection(FinsConnection):
    """
    Serial implementation of FINS protocol connection.
    
    This class handles FINS communication over RS-232/RS-485 serial connections.
    """
    
    def __init__(self, port: str, baudrate: int = 9600, timeout: float = 5.0,
                 bytesize: int = 8, parity: str = 'N', stopbits: int = 1):
        """
        Initialize serial connection.
        
        Args:
            port: Serial port name (e.g., 'COM1', '/dev/ttyUSB0')
            baudrate: Communication speed
            timeout: Read timeout in seconds
            bytesize: Number of data bits
            parity: Parity checking ('N', 'E', 'O')
            stopbits: Number of stop bits
        """
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.serial_conn: Optional[serial.Serial] = None
        self.connected = False
        
        # Set default node addresses for serial
        self.dest_node_add = 0
        self.srce_node_add = 0
    
    def connect(self) -> None:
        """
        Establish serial connection.
        
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits
            )
            
            if self.serial_conn.is_open:
                self.connected = True
                # Clear any existing data in buffers
                self.serial_conn.reset_input_buffer()
                self.serial_conn.reset_output_buffer()
            else:
                raise ConnectionError("Failed to open serial port")
                
        except serial.SerialException as e:
            self.connected = False
            if self.serial_conn:
                self.serial_conn.close()
                self.serial_conn = None
            raise ConnectionError(f"Serial connection failed: {e}")
    
    def disconnect(self) -> None:
        """Close the serial connection."""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except serial.SerialException:
                pass
            finally:
                self.serial_conn = None
                self.connected = False
    
    def execute_fins_command_frame(self, fins_command_frame: bytes) -> bytes:
        """
        Execute a FINS command frame over serial connection.
        
        Args:
            fins_command_frame: Complete FINS command frame
            
        Returns:
            Response frame bytes
            
        Raises:
            ConnectionError: If communication fails
        """
        if not self.connected or not self.serial_conn:
            raise ConnectionError("Serial connection not established")
        
        try:
            # Clear buffers before sending
            self.serial_conn.reset_input_buffer()
            self.serial_conn.reset_output_buffer()
            
            # Send command frame
            bytes_written = self.serial_conn.write(fins_command_frame)
            if bytes_written != len(fins_command_frame):
                raise ConnectionError("Failed to send complete command frame")
            
            # Wait for response
            time.sleep(0.1)  # Small delay for PLC processing
            
            # Read response header first (10 bytes minimum)
            response_data = self.serial_conn.read(14)  # Header + command + end code
            if len(response_data) < 14:
                raise ConnectionError("Incomplete response header")
            
            # Determine if there's additional data to read
            # This is a simplified approach - in practice, you might need
            # to parse the response to determine the exact length
            remaining_data = self.serial_conn.read(1024)  # Read remaining data
            response_data += remaining_data
            
            return response_data
            
        except serial.SerialTimeoutException:
            raise ConnectionError("Serial communication timeout")
        except serial.SerialException as e:
            self.connected = False
            raise ConnectionError(f"Serial communication error: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
