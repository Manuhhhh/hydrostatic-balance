import serial

class SerialHandler:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        
        self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
    
    def send(self, data):
        self.serial.write(data.encode())
