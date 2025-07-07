from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
import time 
def main():

    plc_ip_address = '192.168.2.2'

    
    with FinsUdpConnection(plc_ip_address) as finsudp5:
        try:
            data = finsudp5.cpu_unit_status_read()
            print("CPU Unit Status Read:\n", data['data'])
            msg = finsudp5.cpu_unit_details_read()
            print("CPU Unit Data Read:\n", msg['data'])
            date_time = finsudp5.clock_read()
            print("Clock Read:", date_time['data'])
        except Exception as e:
            print(e)  

    
    with FinsUdpConnection(plc_ip_address, debug=False ) as finsudp6:
        print("-------CIO Area Bit--------")
        data = finsudp6.read('2.01',"int16")
        print("The CIO-2.01 is 1 at this position\n read data ", data['data'][0])   
    
    with FinsUdpConnection(plc_ip_address,debug = False) as finsudp6:
        #Read DM area data
        print("-------DM Area word level--------")
        data = finsudp6.read('D100',"int16")
        print("The D100 is #12 at this position\n read data ", data['data'][0])
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")
