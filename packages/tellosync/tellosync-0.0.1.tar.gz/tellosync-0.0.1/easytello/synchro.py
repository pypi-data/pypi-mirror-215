import serial
import time

class Synchro:
    def __init__(self, port:int) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = 192000
        self.ser.port = f"COM{port}"
        self.ser.open()
    
    def open(self) -> None:
        self.ser.open()

    def close(self) -> None:
        self.ser.close()

    def selfIsReady(self) -> None:
        self.ser.write(b"READY")
    
    def isSynced(self) -> bool:
        return self.ser.readline().decode("Ascii") == "SYNCED"
