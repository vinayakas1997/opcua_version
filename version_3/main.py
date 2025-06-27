from OMRON_FINS_PROTOCOL.Infrastructure.fins.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.components.conversion import *

import time 
def main():
        # def bcd_to_decimal(bcd):
        #     return ((bcd >> 4) * 10) + (bcd & 0x0F)
        # def bcd_to_decimal2(bcd_bytes):
        #     return ((bcd_bytes[0] >> 4) * 1000) + ((bcd_bytes[0] & 0x0F) * 100) + \
        #         ((bcd_bytes[1] >> 4) * 10) + (bcd_bytes[1] & 0x0F)
        with FinsUdpConnection('192.168.137.2') as finsudp:
            for i in range(10):
                data, is_success, msg = finsudp.read('T1000', 1)
                if is_success:
                    print(f"The T1000 present value: {bcd_to_decimal(data)}")   
                else:
                    print(f"Read failed: {msg}")
                time.sleep(0.5)

        with FinsUdpConnection('192.168.137.2') as finsudp2:
            for i in range(10):
                data,_,_ = finsudp2.read('C0001', 1)
                print("The C0001 present value ",toInt16(data))
                time.sleep(5)
                
        

if __name__ == "__main__":
    main()
