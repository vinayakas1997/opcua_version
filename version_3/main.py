from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.exception import *
import time 
def main():

    plc_ip_address = '192.168.2.2'

    
    with FinsUdpConnection(plc_ip_address, debug=False ) as finsudp6:
        print("-------CIO Area Bit--------")
        data = finsudp6.read('2.01',"int16")
        print("The CIO-2.01 is 1 at this position\n read data ", data)   
        

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
