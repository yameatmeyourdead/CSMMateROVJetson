from enum import Enum

class messageType(Enum):
    command = "0001"
    controller = "0000"
    data = "1001"
    camera = "0110"
    message = "1010"