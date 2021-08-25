from enum import Enum

class messageType(Enum):
    command = "0001"
    stop = "1000"
    idle = "0100"
    teleop = "0010"
    auto = "1111"
    controller = "0000"
    data = "1001"
    camera = "0110"
    message = "1010"