from src.hydrostatic_balance.pasco_device import PascoDevice
from src.hydrostatic_balance.serial_handler import SerialHandler
import os
from dotenv import load_dotenv
import keyboard

load_dotenv()

pasco_id = os.getenv("PASCO_ID")
device_port = os.getenv("DEVICE_PORT")
baud_rate = os.getenv("BAUD_RATE")
timeout = os.getenv("TIMEOUT")
max_retries = os.getenv("MAX_RETRIES")
retry_delay = os.getenv("RETRY_DELAY")
debug = os.getenv("DEBUG")

def main():
    device = PascoDevice(pasco_id, max_retries, retry_delay, debug)
    serial = SerialHandler(device_port, baud_rate, timeout, debug)
    
    while True:
        keyboard.wait('space')
        data = device.read_data()
        serial.send(f"FORCE:{data}")
        
        
        
        