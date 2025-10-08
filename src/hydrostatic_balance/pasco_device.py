from pasco.pasco_ble_device import PASCOBLEDevice
import time

class PascoDevice:
    def __init__(self, device_id, max_retries=3, retry_delay=2):
        self.device_id = device_id
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.device = PASCOBLEDevice()
        self.connect()

    def connect(self):
        """Intenta conectar al dispositivo con reintentos."""
        for attempt in range(1, self.max_retries + 1):
            try:
                self.device.connect_by_id(self.device_id)
                print(f"Conectado al dispositivo {self.device_id}")
                return
            except Exception as e:
                print(f"Error conectando al dispositivo (intento {attempt}): {e}")
                time.sleep(self.retry_delay)
        raise ConnectionError(f"No se pudo conectar al dispositivo {self.device_id} después de {self.max_retries} intentos.")

    def read_data(self, measurement_type='Force'):
        """Lee datos de forma segura, reconectando si falla."""
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.device.read_data(measurement_type)
            except Exception as e:
                print(f"Error leyendo {measurement_type} (intento {attempt}): {e}")
                self.device.disconnect()
                time.sleep(self.retry_delay)
                self.connect()
        print(f"No se pudo leer {measurement_type} después de {self.max_retries} intentos.")
        return None

    def disconnect(self):
        try:
            self.device.disconnect()
            print(f"Desconectado del dispositivo {self.device_id}")
        except Exception as e:
            print(f"Error al desconectar: {e}")
