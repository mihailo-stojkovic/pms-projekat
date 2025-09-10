from enum import Enum


class MachineStates(Enum):
    """
    Enum klasa koja definiše stanja mašine stanja.
    """
    INIT = 0
    IDLE = 1
    STD_CALIBRATION = 2
    PEAK_CALIBRATION = 3
    MEASUREMENT = 4
    ERROR = 5
    SHUTDOWN = 6
    EXIT = 7
    UNDEFINED = 8