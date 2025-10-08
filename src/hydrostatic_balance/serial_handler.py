import serial

class SerialHandler:
    def __init__(self, port = "COM5", baud_rate = 9600, timeout = 3, debug=False):
        self.debug = debug
        if debug:
            print(f"Iniciando conexión serial a {port} a {baud_rate} baudios")
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        
        self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        
        if debug:
            print("Conexión del dispositivo serial establecida")
    
    def send(self, data):
        if self.debug:
            print(f"Enviando datos: {data}")
            
        self.serial.write((data + "\n").encode())
        if self.debug:
            print("Listo")
