
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
        from dotenv import load_dotenv
        import os        
        
        load_dotenv()
        
        self.port = port or os.getenv("PORT", "COM3")
        self.baudrate = baudrate or int(os.getenv("BAUDRATE", "9600"))
    
    
    def __open_connection(self):
        import serial
        if self.__com is None:
            try:
                self.__com = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"Opened serial connection on {self.port} at {self.baudrate} baud.")
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.__com = None
    
    
    
    def __read_line(self) -> str | None:
        if self.__com and self.__com.is_open:
            try:
                line = self.__com.readline().decode('utf-8').strip()
                return line
            except Exception as e:
                print(f"Error reading from serial port: {e}")
                return None
        else:
            print("Serial port is not open.")
            return None
    
    
    def __parse_line(self, line: str) -> dict | None:
        from util.InstructionParser import InstructionParser
        try:
            parsed = InstructionParser.parse_instruction(line)
            return parsed
        except ValueError as e:
            print(f"Error parsing line: {e}")
            return None
    
    
    
    @staticmethod
    def initialize(port: str | None = None, baudrate : int = 9600):
        if not SerialComProvider.__instance:
            with SerialComProvider.__class_lock:
                if not SerialComProvider.__instance:
                    SerialComProvider.__instance = SerialComProvider(port, baudrate)
                    SerialComProvider.__instance.__open_connection()
        return SerialComProvider.__instance
    
    
    @staticmethod
    def cleanup():
        if SerialComProvider.__instance and SerialComProvider.__instance.__com:
            SerialComProvider.__instance.__com.close()
            SerialComProvider.__instance.__com = None
            print("Serial connection closed.")