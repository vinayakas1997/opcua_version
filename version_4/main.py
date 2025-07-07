from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.exception import *
import time 
def main():

    plc_ip_address = '192.168.2.2'

    
    # with FinsUdpConnection(plc_ip_address) as finsudp5:
    #     try:
    #         data = finsudp5.cpu_unit_status_read()
    #         print("CPU Unit Status Read:", data)
    #         msg = finsudp5.cpu_unit_details_read()
    #         print("CPU Unit Data Read:", msg)
    #         # data = finsudp5.read('10', 'int16')
    #         # print("Data read:", data)
    #         date_time = finsudp5.clock_read()
    #         print("Clock Read:", date_time)
    #     except FinsDataError as e:
    #         print(e)  # Just print the custom error message without traceback

    
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------CIO Area Word --------")
    #     data,_,_ = finsudp6.read('10',"int16")
    #     print("The CIO-10 is #20 at this position\n read data ", data)
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------CIO Area Bit--------")
    #     data,_,_ = finsudp6.read('10.05',"int16")
    #     print("The CIO-10.05 is 1 at this position\n read data ", data)
    
    with FinsUdpConnection(plc_ip_address, debug=False ) as finsudp6:
        print("-------CIO Area Bit--------")
        data = finsudp6.read('2.01',"int16")
        print("The CIO-2.01 is 1 at this position\n read data ", data)   
        
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------DM Area word level--------")
    #     data,_,_ = finsudp6.read('D100',"int16")
    #     print("The D100 is #12 at this position\n read data ", data)
    
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------DM Area word level--------")
    #     data,_,_ = finsudp6.read('D100',"int16")
    #     print("The D100 is #12 at this position\n read data ", data)
    
    
    # with FinsUdpConnection(plc_ip_address,debug=False) as finsudp6:
    #     print("-------DM Area float --------")
    #     data = finsudp6.read('D200',"float")
    #     print("The D200 is +3.142 at this position\n read data ", data)
        
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------W Area--------")
    #     data,_,_ = finsudp6.read('W1',"int16")
    #     print("The W1 is #56 at this position\n read data ", data)
    
    # with FinsUdpConnection(plc_ip_address) as finsudp6:
    #     #Read CIO area data
    #     print("-------H Area--------")
    #     data,_,_ = finsudp6.read('H1',"int16")
    #     print("The H1 is #78 at this position\n read data ", data)
    
    # with FinsUdpConnection(plc_ip_address) as finsudp7:
    #     #Read Counter area data
    #     print("-------C Area--------")
    #     for i in range(6):
    #         data,_,_ = finsudp7.read('C0001',"int16")
    #         print("The C0001 present value is ", data)
    #         time.sleep(5)  # Wait for 1 second before the next read
        
    # with FinsUdpConnection(plc_ip_address,debug=True) as finsudp5:
    #     try:
    #         data = finsudp5.cpu_unit_status_read()
    #         print("CPU Unit Status Read:", data)
    #         msg = finsudp5.cpu_unit_details_read()
    #         print("CPU Unit Data Read:", msg)
    #         # data = finsudp5.read('10', 'int16')
    #         # print("Data read:", data)
    #         date_time = finsudp5.clock_read()
    #         print("Clock Read:", date_time)
    #     except FinsDataError as e:
    #         print(e)  # Just print the custom error message without traceback
    
    # with FinsUdpConnection(plc_ip_address,debug=True) as finsudp6:
    #     #Read CIO area data
    #     print("-------H Area--------")
    #     data,_,_ = finsudp6.read('H1',"int16")
    #     print("The H1 is #78 at this position\n read data ", data)
    
    # with FinsUdpConnection(plc_ip_address,debug = True) as finsudp6:
    #     #Read DM area data
    #     print("-------DM Area word level--------")
    #     data,_,_ = finsudp6.read('D100',"int16")
    #     print("The D100 is #12 at this position\n read data ", data)
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
