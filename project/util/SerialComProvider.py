
import threading
from util.ComCode import SendComCode

class SerialComProvider:
    """
    Singleton klasa koja obezbeđuje serijsku komunikaciju sa Arduinom.
    Args:
        port (str | None, optional): port na kome je povezan uređaj. Očekivana vrednost je None.
        baudrate (int, optional): Baudrate. Očekivana vrednost je 9600.
    """
    
    __instance = None
    __class_lock = threading.Lock()    
    __maximum_wait_time = 10 # Maksimalno cekanje od 10 sekunde izmedju cekanja
    __increase_delta_time = 1 # Povecanje vremena cekanja za 1 sekundu izmedju neuspesnih pokusaja
    __com = None
    
    def __init__(self, port: str | None = None, baudrate: int = 9600):
        from dotenv import load_dotenv
        import os        
        
        load_dotenv()
        
        self.port = port or os.getenv("PORT", "COM3")
        self.baudrate = baudrate or int(os.getenv("BAUDRATE", "9600"))
        self.__wait_time = 0
    
    def __open_connection(self):
        import serial
        if self.__com is None:
            try:
                self.__com = serial.Serial(self.port, self.baudrate, timeout=1)
                self.__reset_wait()
                print(f"Opened serial connection on {self.port} at {self.baudrate} baud.")
            except serial.SerialException as e:
                print(f"Error opening serial port: {e}")
                self.__wait()                
                self.__com = None
    
    
    
    def read_line(self) -> str | None:
        if self.__com and self.__com.is_open:
            try:
                line = self.__com.readline().decode('utf-8').strip()
                self.__reset_wait()
                return line
            except Exception as e:
                print(f"Error reading from serial port: {e}")
                self.__wait()
                return None
        else:
            print("Serial port is not open.")
            self.__wait()
            return None
    
    
    def parse_line(self, line: str) -> dict | None:
        from util.InstructionParser import InstructionParser
        try:
            parsed = InstructionParser.parse_instruction(line)
            return parsed
        except ValueError as e:
            print(f"Error parsing line: {e}")
            return None
    
    def __reset_wait(self):
        self.__wait_time = 0
    
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
            
    @staticmethod
    def send_command(command : int):
        if SerialComProvider.__instance and SerialComProvider.__instance.__com and SerialComProvider.__instance.__com.is_open:
            print(f"Sending: {command}")
            try:
                SerialComProvider.__instance.__com.write((str(command) + '\n').encode('utf-8'))
                SerialComProvider.__instance.__reset_wait()
                print(f"Sent command: {command}")
            except Exception as e:
                print(f"Error sending command: {e}")
                SerialComProvider.__instance.__wait()
        else:
            print("Serial port is not open. Cannot send command.")
            
            
    def __del__(self):
        if self.__com and self.__com.is_open:
            SerialComProvider.cleanup()
            print("Serial connection closed in destructor.")
            
            
    
    def __wait(self):
        import time
        self.__wait_time += SerialComProvider.__increase_delta_time
        if self.__wait_time >= SerialComProvider.__maximum_wait_time:
            print("Maximum wait time exceeded. No new tries will be initiated")
            raise SystemExit("Error occured: Maximum connection time exceeded")
        print(f"Waiting {self.__wait_time} seconds before trying again.")
        try:
            time.sleep(self.__wait_time)
        except:
            return None
    