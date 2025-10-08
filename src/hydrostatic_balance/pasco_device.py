from pasco.pasco_ble_device import PASCOBLEDevice

class PascoDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.device = PASCOBLEDevice()
        self.device.connect_by_id(device_id)

    def read_data(self, measurement_type = 'Force'):
        return self.device.read_data(measurement_type)
    
    def disconnect(self):
        self.device.disconnect()