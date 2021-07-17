from Components import Component
from tools import Logger

class IMU(Component):
    """Implementation of 9-axis BNO055 IMU"""
    def __init__(self) -> None:
        return
    
    @staticmethod
    def calibrateGyro():
        Logger.log("Calibrating Gyroscope, ensure this occured at a time when robot is completely still")
        # TODO: IMPLEMENT

    def update(self) -> None:
        return

    def autoUpdate(self) -> None:
        return
    
    def kill(self) -> None:
        return