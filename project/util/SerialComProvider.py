
import threading

class SerialComProvider:
    """
    Singleton klasa koja obezbeđuje serijsku komunikaciju sa Arduinom.
    Args:
        port (str | None, optional): port na kome je povezan uređaj. Očekivana vrednost je None.
        baudrate (int, optional): Baudrate. Očekivana vrednost je 9600.
    """
    
    __instance = None
    __class_lock = threading.Lock()    
    
    __com = None
    
    def __init__(self, port: str | None = None, baudrate: int = 9600):
        
        self.port = port
        self.baudrate = baudrate
    
    
    def __open_connection(self):
        import serial
        if self.__com is None:
            try:
                self.__com = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"Opened serial connection on {self.port} at {self.baudrate} baud.")
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.__com = None
    
    
    
    @classmethod
    def initialize(cls, port: str | None = None, baudrate : int = 9600):
        if not cls.__instance:
            with cls.__class_lock:
                if not cls.__instance:
                    cls.__instance = SerialComProvider(port, baudrate)
                    cls.__instance.__open_connection()
        return cls.__instance
    
    
    @staticmethod
    def cleanup():
        if SerialComProvider.__instance and SerialComProvider.__instance.__com:
            SerialComProvider.__instance.__com.close()
            SerialComProvider.__instance.__com = None
            print("Serial connection closed.")