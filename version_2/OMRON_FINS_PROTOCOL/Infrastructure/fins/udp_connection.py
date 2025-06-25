"""
FINS UDP Connection Implementation
==================================
This module provides UDP implementation of the FINS protocol connection.
"""

import socket
from typing import Optional

from ...Fins_domain.connection import FinsConnection

__version__ = "0.1.0"


class FinsUdpConnection(FinsConnection):
    """
    UDP implementation of FINS protocol connection.
    
    This class handles FINS communication over UDP networks.
    """
    
    def __init__(self, host: str, port: int = 9600, timeout: float = 5.0):
        """
        Initialize UDP connection.
        
        Args:
            host: PLC IP address or hostname
            port: UDP port number (default 9600 for FINS)
            timeout: Response timeout in seconds
        """
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connected = False
        
        # Set default node addresses for UDP
        self.dest_node_add = 1
        self.srce_node_add = 254
    
    def connect(self) -> None:
        """
        Initialize UDP socket.
        
        Raises:
            ConnectionError: If socket creation fails
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
            self.connected = True
            
        except socket.error as e:
            self.connected = False
            if self.socket:
                self.socket.close()
                self.socket = None
            raise ConnectionError(f"Failed to create UDP socket: {e}")
    
    def disconnect(self) -> None:
        """Close the UDP socket."""
        if self.socket:
            try:
                self.socket.close()
            except socket.error:
                pass
            finally:
                self.socket = None
                self.connected = False
    
    def execute_fins_command_frame(self, fins_command_frame: bytes) -> bytes:
        """
        Execute a FINS command frame over UDP.
        
        Args:
            fins_command_frame: Complete FINS command frame
            
        Returns:
            Response frame bytes
            
        Raises:
            ConnectionError: If communication fails
        """
        if not self.connected or not self.socket:
            raise ConnectionError("UDP socket not initialized")
        
        try:
            # Send command frame
            self.socket.sendto(fins_command_frame, (self.host, self.port))
            
            # Receive response
            response_data, addr = self.socket.recvfrom(4096)
            
            # Verify response came from expected address
            if addr[0] != self.host:
                raise ConnectionError(f"Response from unexpected address: {addr[0]}")
            
            return response_data
            
        except socket.timeout:
            raise ConnectionError("UDP communication timeout")
        except socket.error as e:
            raise ConnectionError(f"UDP communication error: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
