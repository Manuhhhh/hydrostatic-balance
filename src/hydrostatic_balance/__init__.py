from src.hydrostatic_balance.pasco_device import PascoDevice
from src.hydrostatic_balance.serial_handler import SerialHandler
import os
from dotenv import load_dotenv
import keyboard

load_dotenv()

pasco_id = os.getenv("PASCO_ID")

def main():
    device = PascoDevice(pasco_id)
    serial = SerialHandler(port="COM5", baud_rate=9600, timeout=2)
    
    while True:
        keyboard.wait('space')
        data = device.read_data()
        serial.send(data)
        
        
        
        