import threading
from util.StateMachine import StateMachine
from util.SerialComProvider import SerialComProvider


class MachineStateManager:
    __instance = None
    __class_lock = threading.Lock()
    
    
    
    def __init__(self):
        self.__state_machine = StateMachine.initialize()
        self.__serial_provider = SerialComProvider.initialize()
        
    @classmethod
    def initialize(cls):
        if not cls.__instance:
            with cls.__class_lock:
                if not cls.__instance:
                    cls.__instance = MachineStateManager()
        return cls.__instance