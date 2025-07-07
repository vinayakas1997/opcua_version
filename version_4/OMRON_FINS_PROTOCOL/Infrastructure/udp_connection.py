"""
FINS UDP Connection Implementation
==================================
This module provides UDP implementation of the FINS protocol connection.
"""
from datetime import datetime
import socket
from typing import Optional,Tuple,Union,Any

# Fix the import path - adjust based on your actual project structure
from OMRON_FINS_PROTOCOL.Fins_domain.connection import FinsConnection
from OMRON_FINS_PROTOCOL.Fins_domain.command_codes import FinsCommandCode
from OMRON_FINS_PROTOCOL.Fins_domain.frames import FinsResponseFrame
from OMRON_FINS_PROTOCOL.Fins_domain.fins_error import FinsResponseError
from OMRON_FINS_PROTOCOL.Fins_domain.mem_address_parser import FinsAddressParser
from OMRON_FINS_PROTOCOL.components import *
from OMRON_FINS_PROTOCOL.exception import *

__version__ = "0.1.0"


class FinsUdpConnection(FinsConnection):
    """
    UDP implementation of FINS protocol connection.
    
    This class handles FINS communication over UDP networks.
    """
    
    def __init__(self, host: str, port: int = 9600, timeout: int = 5,
                 dest_network: int = 0, dest_node: int = 0, dest_unit: int = 0,
                 src_network: int = 0, src_node: int = 1, src_unit: int = 0,
                 destfinsadr: str = "0.0.0", srcfinsadr: str = "0.1.0",debug = False):
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
        # debugging mode 
        self.debug = debug
    
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
            if self.debug == True:
                # Send command frame
                print("  Sending FinsCommand frame (The complete frame): ", fins_command_frame)
                print("  FinsCommand Destination address(IP,port): " , self.addr)
            self.socket.sendto(fins_command_frame, self.addr)
            
            # Receive response
            response_data = self.socket.recv(4096)
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
        
    # def read(self, memory_area_code, readsize: int = 4, _type: str = 'INT16' ,service_id: int = 0 ) -> Tuple[Union[bytes, bool],bool,str]:
    def read(self, memory_area_code, _type: str = 'INT16' ,service_id: int = 0 ) -> Tuple[Any,bool,str]:
        """
        Read data from PLC memory area using FINS command codes.
        
        Args:
            memory_area_code: Memory area identifier
            address: Starting address
            count: Number of items to read
            
        Returns:
            Response data
        """
        
        data_type_mapping = {
            'INT16' : [1, toInt16],
            'UINT16' : [1, toUInt16],
            'INT32' : [2, toInt32],
            'UINT32' : [2, toUInt32],
            'INT64' : [4, toInt64],
            'UINT64' : [4, toUInt64],
            'FLOAT' : [2, toFloat],
            'DOUBLE' : [4, toDouble],
            'bcd_to_decimal' : [1,bcd_to_decimal]
        }
        
        # data_type_mapping = {
        #     'I16' : [1, toInt16],
        #     'UI16' : [1, toUInt16],
        #     'I32' : [2, toInt32],
        #     'UI32' : [2, toUInt32],
        #     'I64' : [4, toInt64],
        #     'UI64' : [4, toUInt64],
        #     'F' : [2, toFloat],
        #     'D' : [4, toDouble],
        #     'BCD2D' : [1,bcd_to_decimal]
        # }
        
         # Normalize type_
        if _type is not None:
            _type = _type.upper()
            if _type not in data_type_mapping:
                raise FinsDataError(
                        f"Invalid data type: '{_type}'. Allowed types are: {', '.join(data_type_mapping.keys())}",
                        error_code="INVALID_TYPE"
                        )
        else:
            _type = 'INT16'

        if '.' in memory_area_code:
            readsize = 1
        else:
            readsize = data_type_mapping[_type][0]
        conversion_function = data_type_mapping[_type][1]     
        readnum = readsize // 990
        remainder = readsize % 990
        
        data = bytes() # Initialize accumulator for all read data
        for cnt in range(readnum + 1):
            info = self.address_parser.parse(memory_area_code,cnt * 990)
            if self.debug == True:
                print("----------DEBUG MODE -------------")
                print(f"  Address Given: {memory_area_code}")
                print(f"  Type: {info['address_type']}")
                print(f"  Memory Area: {info['memory_area']}")
                print(f"  Word Address: {info['word_address']}")
                print(f"  Bit Number: {info['bit_number']}")
                print(f"  Memory Type Code: {info['memory_type_code']}")
                print(f"  Offset Bytes: {info['offset_bytes']}")
                print(f"  Fins_Format: {info['fins_format']}") 
            
            if cnt == readnum:
                rsize = list(int(remainder).to_bytes(2,'big'))
            else:
                rsize = list(int(990).to_bytes(2,'big'))
            
            sid = service_id.to_bytes(1,'big')
            
            # creating the command_frame 
            finsary = bytearray(8)
            finsary[0:2] = self.command_codes.MEMORY_AREA_READ
            finsary[2] = info['memory_type_code']
            finsary[3:5] = info['offset_bytes']
            if info['address_type'] == 'bit':
                finsary[5] = info['bit_number']
            else:
                finsary[5] = 0x00
            finsary[6] = rsize[0]
            finsary[7] = rsize[1]
            
            # Build FINS command frame using the command code
            command_frame = self.fins_command_frame(command_code=finsary,service_id=sid)   
            response_data = self.execute_fins_command_frame(command_frame)
            response_frame = self._parse_response(response_data)
            is_success, msg = self._check_response(response_frame.end_code)
            
            if is_success:
                data += response_frame.text
            
            else:
                # An error occurred during this chunk read
                print(f"Error Occurred at chunk {cnt*990}: {msg}")
                # Return the data accumulated so far, along with the error status and message
                converted_data = conversion_function(data)
                return converted_data, is_success, msg
        
        # If the loop completes, all chunks were read successfully
        if len(data) % 2 != 0:
            data = b'\x00' + data
        # print("Len ->",len(data), "    Data ->", data)
        converted_data = conversion_function(data)
        return converted_data, True, 'Read successful'
    
    
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def cpu_unit_details_read(self) -> dict:
        """
        Read CPU unit details.
        PLC is reachable over the network
        FINS protocol communication is working
        The PLC responded without any error
        The PLC's CPU unit is in a normal state (e.g., not in error or program stop mode)
        Returns:
            Tuple of (status, message)
        """
        # Command code for CPU unit data status read
        command_code = self.command_codes.CPU_UNIT_DATA_READ
        
        # Build FINS command frame
        command_frame = self.fins_command_frame(command_code=command_code)
        data_dict = dict()
        try:
            rcv = self.execute_fins_command_frame(command_frame)
            response_data = rcv[10:]
            # print("from response cpu unit data read", rcv)
            data = response_data[4:]  # Skip 4 bytes (command + end code)

            unit_name = data[0:20].decode().strip()
            boot_version = data[20:25].decode().strip()
            os_version = data[32:37].decode().strip()
            if response_data[2:4] == b'\x00\x00':
                data_dict['FINS response'] = 'Normal'
                data_dict['unit_name'] = unit_name
                data_dict['boot_version'] = boot_version
                data_dict['os_version'] = os_version
            else:
                data_dict['FINS response'] = 'Error'
                data_dict['Error Code'] = response_data[2:4].hex()
            
            if self.debug == True:
                print("\n ------------CPU Unit Data Read Response------------")
                print("  Whole Response Data:", response_data)
                print("  Data after header and command:", data)
                print("  Command code:", response_data[10:12])
                print("  FINS response status:", response_data[12:14])
                print("  Unit Name:", unit_name)
                print("  Boot Version:", boot_version)
                print("  OS Version:", os_version)
                print(" ------------End of CPU Unit Data Read Response------------\n")
            
            
                
            return data_dict

        except ConnectionError as e:
            return data_dict
        except Exception as e:
            return data_dict
        
    def cpu_unit_status_read(self) -> Tuple[bool, dict]:
        """
        Read CPU unit status.
        response_data [10:]
        Data format:
        response_data[0:2] Command code = 0x06 0x01
        response_data[2:4] Status = 0x00 0x00 for success, or other codes for errors
        
        response_data [4:6] Next two bytes are the parameters:
        1st byte Status (response)
        00: Stop 
        01: Run
        80: CPU on standby (the start switch is OFF or the CPU is waiting for a signal from a device such as a Remote I/O Slave Unit).

        2nd byte 
        Mode (response): One of the following PC modes:
        00: PROGRAM
        02: MONITOR
        04: RUN
        
        response_data[6:8] fatal error data 
        0x00 0x00 for no errors, or other codes for errors - refer the FINS manual for details.
        
        response_data[8:10] Non fatal error data
        the first byte is always the x00
        the second byte is the error priority decimal number [00 - 99]
        
        """
        #Mode_dict 
        mode_code_dict = {  b'\x00': 'PROGRAM',
                            b'\x02': 'MONITOR',
                            b'\x04': 'RUN',
                        }   
        # Status_dict
        status_code_dict = { b'\x00': 'Stop',
                            b'\x01': 'Run',
                            b'\x80': 'CPU on standby',
                            b'\x05': 'No data available'
                    }
        # Command code for CPU unit data status read
        command_code = self.command_codes.CPU_UNIT_STATUS_READ
        
        # Build FINS command frame
        command_frame = self.fins_command_frame(command_code=command_code)
        status_dict = dict()
        try:
            response_data = self.execute_fins_command_frame(command_frame)
            # print("from response cpu unit status read", response_data)
            data = response_data[12:]  # Skip 12 bytes (header + command + end code)
            
            if self.debug == True:
                print("\n ------------CPU Unit Status Read Response------------")
                print("  Whole Response Data:", response_data)
                print("  Data after header and command:", response_data[10:])
                print("  Command code:",response_data[10:12])
                print("  Response status:", response_data[12:14])
                print("  Next two bytes are the parameters:")
                print("  1st byte Status (response):", response_data[14:15])
                print("  Mode (response):", response_data[15:16])
                print("  fatal error data:", response_data[16:18])
                print("  Non fatal error data:", response_data[18:20])
                print("  Non fatal error data priority:", response_data[19:20])
                print(" ------------End of CPU Unit Status Read Response------------\n")

            if response_data[12:14] == b'\x00\x00':
                status_dict['FINS response'] = 'Normal'
                # print("Raw status byte:", response_data[14:15])
                # print("Raw mode byte:", response_data[15:16])
                status_dict['Status'] = status_code_dict.get(response_data[14:15], 'Unknown Status')
                status_dict['Mode'] = mode_code_dict.get(response_data[15:16], 'Unknown Mode')
                # status_dict['Mode'] = response_data[15:16].hex()
            
            else:
                status_dict['FINS response'] = 'Error'
                status_dict['Error Code'] = response_data[12:14].hex()
                
            return True, status_dict
            
        except ConnectionError as e:
            return False, status_dict
        except Exception as e:
            return False, status_dict
        
    def clock_read(self) -> Union[datetime, str]:
        # def clock_read(self) -> Tuple[bool,str]:
    # def clock_read(self) -> datetime:
        """
        Read PLC clock.
        
        Returns:
            Tuple of (status, message)
        """
        # Command code for clock read
        command_code = self.command_codes.CLOCK_READ
        
        # Build FINS command frame
        command_frame = self.fins_command_frame(command_code=command_code)
        
        try:
            rcv = self.execute_fins_command_frame(command_frame)
            finsres = rcv[10:]

            if finsres[2] == 0x00 and finsres[3] == 0x00:
                dtAry = finsres[4:10]
                dtStr = dtAry.hex()
                PlcDateTime = datetime.strptime(dtStr, '%y%m%d%H%M%S')
            else:
                PlcDateTime = FinsResponseError(finsres[2:4]).message
            # print("PLC Date Time:", PlcDateTime)
            return PlcDateTime
        #     response_frame = self._parse_response(response_data)
        #     is_success, msg = self._check_response(response_frame.end_code)
        #     return is_success, msg
        except ConnectionError as e:
            return str(e)
        except Exception as e:
            return str(e)