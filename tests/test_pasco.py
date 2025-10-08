from time import sleep
from src.hydrostatic_balance.pasco_device import PascoDevice
import os
from dotenv import load_dotenv

load_dotenv()

pasco_id = os.getenv("PASCO_ID", "12345")
max_retries = int(os.getenv("MAX_RETRIES", 5))
retry_delay = int(os.getenv("RETRY_DELAY", 2))
debug = os.getenv("DEBUG") == "True"

def test_connect():
    device = PascoDevice(pasco_id, max_retries, retry_delay, debug)
    assert device.connected == True
    
    while device.connected:
        print(device.read_data())
        sleep(1)