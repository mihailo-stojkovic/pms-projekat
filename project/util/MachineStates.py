from enum import Enum


class MachineStates(Enum):
    """
    Enum klasa koja definiše stanja mašine stanja.
    """
    INIT = 0
    STD_CALIBRATION = 1
    IDLE = 2
    PEAK_DETECTION = 4
    MEASUREMENT = 5
    ERROR = 6
    SHUTDOWN = 7
    EXIT = 8
    UNDEFINED = 9