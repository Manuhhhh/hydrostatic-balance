from pasco.pasco_ble_device import PASCOBLEDevice
import os
from dotenv import load_dotenv

load_dotenv()

pasco_id = os.getenv("PASCO_ID")

def main():
    dev = PASCOBLEDevice()
    dev.connect_by_id(pasco_id)
    print(dev.get_measurement_list())
    print(dev.read_data('Force'))
    dev.disconnect()