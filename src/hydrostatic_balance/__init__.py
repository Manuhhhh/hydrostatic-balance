from pasco.pasco_ble_device import PASCOBLEDevice
import os
from dotenv import load_dotenv

load_dotenv()

pasco_id = os.getenv("PASCO_ID")

def main():
    print(pasco_id)
    # dev = PASCOBLEDevice()
    # dev.connect_by_id("")
    # print(dev.get_measurement_list())
    # print(dev.read_data('Force'))
    # dev.disconnect()