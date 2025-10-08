from src.hydrostatic_balance.density_calculator import ArquimedesCalculator
from src.hydrostatic_balance.pasco_device import PascoDevice
from src.hydrostatic_balance.serial_handler import SerialHandler
import os
from dotenv import load_dotenv
import keyboard

load_dotenv()

pasco_id = os.getenv("PASCO_ID")
device_port = os.getenv("DEVICE_PORT")
baud_rate = int(os.getenv("BAUD_RATE"))
timeout = int(os.getenv("TIMEOUT"))
max_retries = int(os.getenv("MAX_RETRIES"))
retry_delay = int(os.getenv("RETRY_DELAY"))
debug = os.getenv("DEBUG") == "True"
g_val = float(os.getenv("G_VAL"))
water_density = float(os.getenv("WATER_DENSITY"))

def main():
    device = PascoDevice(pasco_id, max_retries, retry_delay, debug)
    serial = SerialHandler(device_port, baud_rate, timeout, debug)
    arquimedes_calculator = ArquimedesCalculator(g_val, water_density)
    
    while True:
        lcd1Vals = []
        print("Press space to read first force value...")
        keyboard.wait('space')
        data = device.read_data()
        if data is None:
            print("Could not read data from device. Retrying...")
            continue
        Wa_val = float(data)
        print("Press space to read second force value...")
        keyboard.wait('space')
        data = device.read_data()
        if data is None:
            print("Could not read data from device. Retrying...")
            continue
        Ws_val = float(data)
        
        E_val = arquimedes_calculator.calculate_buoyant_force(Wa_val, Ws_val)
        
        V_val = arquimedes_calculator.calculate_volume(Wa_val, Ws_val)
        
        D_val = arquimedes_calculator.calculate_density(Wa_val, Ws_val)
        
        dataString = f"DATA:Wa:{Wa_val:.2f}N,Ws:{Ws_val:.2f}N-E:{E_val:.2f}N,V:{V_val:.6f}-Densidad:,D:{D_val:.2f}kg/m3"
        
        serial.send(dataString)
        
        print("Data sent:", dataString)
        
        
        