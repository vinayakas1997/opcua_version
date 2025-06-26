from OMRON_FINS_PROTOCOL.Infrastructure.fins.udp_connection import FinsUdpConnection
import time 
def main():
        with FinsUdpConnection('192.168.137.2') as finsudp:
            # The connect() method is automatically called here
            data, is_success, msg = finsudp.read('T1000', 1)
            if is_success:
                print(f"Read successful: {data}")
            else:
                print(f"Read failed: {msg}")
        
    # The disconnect() method is automatically called here when exiting the 'with' block
    # even if an error occurred inside the block.

if __name__ == "__main__":
    main()
