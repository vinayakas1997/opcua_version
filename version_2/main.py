from OMRON_FINS_PROTOCOL.Infrastructure.fins.udp_connection import FinsUdpConnection





def main():
    finsudp = FinsUdpConnection('192.168.137.2')
    finsudp.connect()
    data = finsudp.read('D0100',1)
    print(data)

if __name__ == "__main__":
    main()