from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.components import *
from OMRON_FINS_PROTOCOL.exception import *
# from OMRON_FINS_PROTOCOL.exception import FinsTimeoutError

import time 
def main():
        with FinsUdpConnection('192.168.137.2') as finsudp5:
            try:
                data = finsudp5.read('10', 'i16')
                print("Data read:", data)
            except FinsDataError as e:
                print(e)  # Just print the custom error message without traceback
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','uint16')
        #     print("Type = uint16",data)
            
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','int32')
        #     print("Type = int32",data)
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','uint32')
        #     print("Type = uint32",data)
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','int64')
        #     print("Type = int64",data)
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','uint64')
        #     print("Type = uint64",data)
        
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','float')
        #     print("Type = float",data)
            
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     data = finsudp5.read('10','double')
        #     print("Type = double",data)
                
        #     print("TheW1 actual stores value #20 the expected value 32\n value read  ",toInt16(data))
        #     # raise FinsTimeoutError()
        # with FinsUdpConnection('192.168.137.2') as finsudp6:
        #     #Read CIO area data
        #     print("-------CIO Area--------")
        #     data,_,_ = finsudp6.read('10.05',1)
        #     print("The CIO-10.05 is 1 at this position\n read data ", data)
        
        # with FinsUdpConnection('192.168.137.2',debug=False) as finsudp6:
        #     print("-------CIO Area--------")
        #     data = finsudp6.read('2.01',"i16")
        #     print("The CIO-2.01 is 1 at this position\n read data ", data)
            
        
        
            
            
        
if __name__ == "__main__":
    main()
