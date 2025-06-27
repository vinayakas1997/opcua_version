"""
FINS TCP Connection Implementation
==================================
This module provides TCP/IP implementation of the FINS protocol connection.
"""

import socket
import time
from typing import Optional

from ...Fins_domain.connection import FinsConnection

__version__ = "0.1.0"


class FinsTcpConnection(FinsConnection):
    """
    TCP/IP implementation of FINS protocol connection.
    
    This class handles FINS communication over TCP/IP networks.
    """
    
    def __init__(self, host: str, port: int = 9600, timeout: float = 10.0):
        """
        Initialize TCP connection.
        
        Args:
            host: PLC IP address or hostname
            port: TCP port number (default 9600 for FINS)
            timeout: Connection timeout in seconds
        """
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connected = False
    
    def connect(self) -> None:
        """
        Establish TCP connection to the PLC.
        
        Raises:
            ConnectionError: If connection fails
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            
            # Perform FINS handshake if needed
            self._perform_handshake()
            
        except socket.error as e:
            self.connected = False
            if self.socket:
                self.socket.close()
                self.socket = None
            raise ConnectionError(f"Failed to connect to {self.host}:{self.port} - {e}")
    
    def disconnect(self) -> None:
        """Close the TCP connection."""
        if self.socket:
            try:
                self.socket.close()
            except socket.error:
                pass
            finally:
                self.socket = None
                self.connected = False
    
    def _perform_handshake(self) -> None:
        """
        Perform FINS TCP handshake to establish node addresses.
        
        Raises:
            ConnectionError: If handshake fails
        """
        # FINS TCP handshake frame
        handshake_frame = b'FINS' + b'\x00\x00\x00\x0C' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x00'
        
        try:
            self.socket.send(handshake_frame)
            response = self.socket.recv(24)
            
            if len(response) < 24:
                raise ConnectionError("Invalid handshake response length")
            
            # Extract node addresses from handshake response
            if response[:4] == b'FINS':
                # Parse response to get assigned node addresses
                self.srce_node_add = response[19]  # Client node address
                self.dest_node_add = response[23]  # Server node address
            else:
                raise ConnectionError("Invalid handshake response format")
                
        except socket.error as e:
            raise ConnectionError(f"Handshake failed: {e}")
    
    def execute_fins_command_frame(self, fins_command_frame: bytes) -> bytes:
        """
        Execute a FINS command frame over TCP.
        
        Args:
            fins_command_frame: Complete FINS command frame
            
        Returns:
            Response frame bytes
            
        Raises:
            ConnectionError: If communication fails
        """
        if not self.connected or not self.socket:
            raise ConnectionError("Not connected to PLC")
        
        try:
            # Send FINS TCP header + command frame
            tcp_header = b'FINS' + len(fins_command_frame).to_bytes(4, 'big') + b'\x00\x00\x00\x02'
            full_frame = tcp_header + fins_command_frame
            
            self.socket.send(full_frame)
            
            # Receive TCP header first
            tcp_response_header = self.socket.recv(16)
            if len(tcp_response_header) < 16:
                raise ConnectionError("Invalid TCP response header")
            
            # Extract response length
            response_length = int.from_bytes(tcp_response_header[8:12], 'big')
            
            # Receive FINS response frame
            response_frame = self.socket.recv(response_length)
            if len(response_frame) < response_length:
                raise ConnectionError("Incomplete response frame")
            
            return response_frame
            
        except socket.error as e:
            self.connected = False
            raise ConnectionError(f"Communication error: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
