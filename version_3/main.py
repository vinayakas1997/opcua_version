from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.components import *
# from OMRON_FINS_PROTOCOL.exception import FinsTimeoutError

import time 
def main():
        # with FinsUdpConnection('192.168.137.2') as finsudp5:
        #     #Read CIO area data
        #     print("-------CIO Area--------")
        #     data,_,_ = finsudp5.read('10',1)
        #     print("TheW1 actual stores value #20 the expected value 32\n value read  ",toInt16(data))
        #     # raise FinsTimeoutError()
        # with FinsUdpConnection('192.168.137.2') as finsudp6:
        #     #Read CIO area data
        #     print("-------CIO Area--------")
        #     data,_,_ = finsudp6.read('10.05',1)
        #     print("The CIO-10.05 is 1 at this position\n read data ", data)
        
        with FinsUdpConnection('192.168.137.2',debug=True) as finsudp6:
            print("-------CIO Area--------")
            data,_,_ = finsudp6.read('2.01',1)
            print("The CIO-2.01 is 1 at this position\n read data ", data)
            
        
        
            
            
        
if __name__ == "__main__":
    main()
