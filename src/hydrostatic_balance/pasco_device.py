from pasco.pasco_ble_device import PASCOBLEDevice
import time

class PascoDevice:
    def __init__(self, device_id, max_retries=3, retry_delay=2, debug=False):
        self.debug = debug
        if debug:
            print(f"Iniciando conexión con el dispositivo Pasco ID: {device_id}")
        self.initial_offset = 0.0
        self.device_id = device_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.device = PASCOBLEDevice()
        self.connect()
        self.calibrate()
        if debug:
            print(f"Conectado al dispositivo Pasco ID: {device_id}")

    def calibrate(self):
        vals = []
        for _ in range(5):
            data = self.device.read_data("Force")
            if data is not None:
                vals.append(float(data))

        average = sum(vals) / len(vals)
        
        self.initial_offset = average

    def connect(self):
        for attempt in range(1, self.max_retries + 1):
            try:
                self.device.connect_by_id(self.device_id)
                self.connected = True
                
                if self.debug:
                    print(f"Conectado al dispositivo {self.device_id}")
                return
            except Exception as e:
                self.connected = False
                if self.debug:
                    print(f"Error conectando al dispositivo (intento {attempt}): {e}")
                time.sleep(self.retry_delay)
        raise ConnectionError(f"No se pudo conectar al dispositivo {self.device_id} después de {self.max_retries} intentos.")

    def read_data(self, measurement_type='Force'):
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.device.read_data(measurement_type)
            except Exception as e:
                if self.debug:
                    print(f"Error leyendo {measurement_type} (intento {attempt}): {e}")
                self.device.disconnect()
                self.connected = False
                time.sleep(self.retry_delay)
                self.connect()
                self.connected = True
        if self.debug:
            print(f"No se pudo leer {measurement_type} después de {self.max_retries} intentos.")
        return None
    
    def get_calibrated_data(self, measurement_type='Force'):
        data = self.read_data(measurement_type)
        if data is not None:
            return_value = -(float(data) - self.initial_offset)
            if return_value < 0:
                return_value = 0
            return round(return_value, 2)
        else:
            return None
    
    def get_unit(self):
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.device.get_measurement_unit("Force")
            except Exception as e:
                if self.debug:
                    print(f"Error obteniendo unidad de medida (intento {attempt}): {e}")
                self.device.disconnect()
                self.connected = False
                time.sleep(self.retry_delay)
                self.connect()
                self.connected = True

    def disconnect(self):
        try:
            self.device.disconnect()
            self.connected = False
            if self.debug:
                print(f"Desconectado del dispositivo {self.device_id}")
        except Exception as e:
            if self.debug:
                print(f"Error al desconectar: {e}")
