"""
FINS UDP Connection Implementation
==================================
This module provides UDP implementation of the FINS protocol connection.
"""

import socket
from typing import Optional,Tuple,Union

# Fix the import path - adjust based on your actual project structure
from OMRON_FINS_PROTOCOL.Fins_domain.connection import FinsConnection
from OMRON_FINS_PROTOCOL.Fins_domain.command_codes import FinsCommandCode
from OMRON_FINS_PROTOCOL.Fins_domain.frames import FinsResponseFrame
from OMRON_FINS_PROTOCOL.Fins_domain.fins_error import FinsResponseError
from OMRON_FINS_PROTOCOL.Fins_domain.mem_address_parser import FinsAddressParser
__version__ = "0.1.0"


class FinsUdpConnection(FinsConnection):
    """
    UDP implementation of FINS protocol connection.
    
    This class handles FINS communication over UDP networks.
    """
    
    def __init__(self, host: str, port: int = 9600, timeout: float = 5.0,
                 dest_network: int = 0, dest_node: int = 0, dest_unit: int = 0,
                 src_network: int = 0, src_node: int = 1, src_unit: int = 0,
                 destfinsadr: str = "", srcfinsadr: str = ""):
        """
        Initialize UDP connection.
        
        Args:
            host: PLC IP address or hostname
            port: UDP port number (default 9600 for FINS)
            timeout: Response timeout in seconds
            dest_network: Destination network address
            dest_node: Destination node address  
            dest_unit: Destination unit address
            src_network: Source network address
            src_node: Source node address
            src_unit: Source unit address
            destfinsadr: Alternative destination address format
            srcfinsadr: Alternative source address format
        """
        # Call parent constructor with proper parameters
        super().__init__(
            host=host, 
            port=port,
            dest_network=dest_network,
            dest_node=dest_node, 
            dest_unit=dest_unit,
            src_network=src_network,
            src_node=src_node,
            src_unit=src_unit,
            destfinsadr=destfinsadr,
            srcfinsadr=srcfinsadr
        )
        
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connected = False
        # Get Fins Command Code 
        self.command_codes = FinsCommandCode()
        # Initialize address parser
        self.address_parser = FinsAddressParser()
    
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
            
        raises:
            ConnectionError: If communication fails
        """
        if not self.connected or not self.socket:
            raise ConnectionError("UDP socket not initialized")
        
        try:
            # Send command frame
            self.socket.sendto(fins_command_frame, self.addr)
            
            # Receive response
            response_data, addr = self.socket.recvfrom(4096)
            
            # Verify response came from expected address
            if addr[0] != self.addr[0]:
                raise ConnectionError(f"Response from unexpected address: {addr[0]}")
            
            return response_data
            
        except socket.timeout:
            raise ConnectionError("UDP communication timeout")
        except socket.error as e:
            raise ConnectionError(f"UDP communication error: {e}")
        
    def _parse_response(self, response_data: bytes) -> FinsResponseFrame:
        """
        Parse response data using FinsResponseFrame.
        
        Args:
            response_data: Raw response bytes from PLC
            
        Returns:
            Tuple of (parsed_response, is_success)
        """
        response_frame = FinsResponseFrame()
        response_frame.from_bytes(response_data)
        
        # Check if command was successful (end code 0x0000 means success)
        # is_success = response_frame.end_code == b'\x00\x00'
        
        return response_frame
    
    def _check_response(self,response_data_end_code:bytes) -> Tuple[bool,str]:
        if response_data_end_code == b'\x00\x00':
            return True, 'Service success'
        elif response_data_end_code == b'\x00\x01':
            return False, 'Service Cancelled'
        else:
            # Use your custom FinsResponseError class
            try:
                error = FinsResponseError(response_data_end_code)
                return False, str(error)
            except Exception:
                # Fallback if error code not recognized
                return False, f"Unknown FINS error: {response_data_end_code}"
        
    
    def read(self, memory_area_code, count: int, service_id: int = 1 ) -> Tuple[Union[bytes, bool],bool,str]:
        """
        Read data from PLC memory area using FINS command codes.
        
        Args:
            memory_area_code: Memory area identifier
            address: Starting address
            count: Number of items to read
            
        Returns:
            Response data
        """
        
        info = self.address_parser.parse(memory_area_code,count)
        rsize = list(int(count).to_bytes(2,'big'))
        sid = service_id.to_bytes(1,'big')
        # creating the command_frame 
        finsary = bytearray(8)
        finsary[0:2] = self.command_codes.MEMORY_AREA_READ
        finsary[2] = info['memory_type_code']
        finsary[3:5] = info['offset_bytes']
        finsary[5] = 0x00
        finsary[6] = rsize[0]
        finsary[7] = rsize[1]
        
        # Build FINS command frame using the command code
        command_frame = self.fins_command_frame(command_code=finsary,service_id=sid)        
        # Execute command
        response_data = self.execute_fins_command_frame(command_frame)
        # Parse response using FinsResponseFrame
        response_frame = self._parse_response(response_data)
        is_success, msg = self._check_response(response_frame.end_code)
        if is_success:
            return response_frame.text,is_success,msg
        else:
            # error_msg = self._get_error_message(response_frame.end_code)
            return b'', is_success, msg
        
    
    
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
