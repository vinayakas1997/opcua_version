from OMRON_FINS_PROTOCOL.Infrastructure.udp_connection import FinsUdpConnection
from OMRON_FINS_PROTOCOL.exception import *
from opcua import Client
from opcua_json import OpcuaAutoNodeMapper
import time
from datetime import datetime

def periodic_sync(fins, opcua_manager, address_mappings, interval_sec):
    try:
        while True:
            for mapping in address_mappings:
                plc_address = mapping['plc_reg_add']
                opcua_tag = mapping['opcua_reg_add']
                data_type = mapping.get('data_type', 'int16')
                bool_temp = False 
                if data_type == 'bool':
                    data_type = 'int16'
                    bool_temp = True
                try:
                    # Read from PLC
                    pack_plc_value = fins.read(plc_address, data_type=data_type)
                    if bool_temp:
                        plc_value = bool(pack_plc_value['data'][0])
                        bool_temp = False
                    else:
                        plc_value = pack_plc_value['data'][0]
                    
                    print(f"[{datetime.now()}] PLC Value ({plc_address}): {plc_value}")

                    # Write to OPC UA
                    opcua_manager.write(opcua_tag, plc_value)
                    print(f"[{datetime.now()}] → Written to OPC UA node: {opcua_tag}")
                except Exception as e:
                    print(f"[{datetime.now()}] ❌ Error processing {plc_address} → {opcua_tag}: {e}")

            # Wait for next full cycle
            time.sleep(interval_sec)

    except KeyboardInterrupt:
        print("Stopped by user.")

def main():
    plc_ip = '192.168.2.2'
    opcua_url = "opc.tcp://192.168.1.20:4840"

    # Multiple mappings: Omron address → OPC UA tag
    address_mappings = [
        {'plc_reg_add': '2.01', 'data_type':'int16','opcua_reg_add': 'CIO201'},
        {'plc_reg_add': 'C0001', 'data_type':'int16','opcua_reg_add': 'C0001'},
        # {'plc': '2.03', 'opcua': 'iVar03'},
    ]

    interval_sec = 1  # seconds

    with FinsUdpConnection(plc_ip, debug=False) as fins:
        client = Client(opcua_url)
        client.connect()
        print("Connected to OPC UA server")

        opcua_manager = OpcuaAutoNodeMapper(client)

        periodic_sync(fins, opcua_manager, address_mappings, interval_sec)

        client.disconnect()
        print("Disconnected from OPC UA server")

if __name__ == "__main__":
    main()
