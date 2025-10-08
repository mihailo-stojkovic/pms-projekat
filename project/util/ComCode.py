from enum import IntEnum

class RecComCode(IntEnum):
    DATA = 1    #Standardni podaci ax, ay, az, touched
    REC_CAL = 2  #Podaci za kalibraciju

class SendComCode(IntEnum):
    STD = 0x01
    CAL = 0x02
    STEP = 0x03