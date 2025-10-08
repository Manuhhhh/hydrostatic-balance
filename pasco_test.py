from pasco.pasco_ble_device import PASCOBLEDevice

dev = PASCOBLEDevice()
dev.connect_by_id("")
print(dev.get_measurement_list())
print(dev.read_data('Force'))
dev.disconnect()