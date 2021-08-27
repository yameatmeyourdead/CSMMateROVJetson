from Components import Component
from tools import Logger
import board
import adafruit_bno055

class IMU(Component):
    """Implementation of 9-axis BNO055 IMU and Depth Sensor for Translational/Rotational Velocity Calculations and Rotational Orientation"""
    def __init__(self) -> None:
        self.BNO055 = adafruit_bno055.BNO055_I2C(board.I2C())
    
    @staticmethod
    def calibrateGyro():
        Logger.log("Calibrating Gyroscope, ensure this occured at a time when robot is completely still")
        # TODO: IMPLEMENT
    
    def getTemp(self):
        return self.BNO055.temperature
    
    def getEulerAngles(self):
        return self.BNO055.euler

    def getQuaternion(self):
        return self.BNO055.quaternion
    
    def getGravity(self):
        return self.BNO055.gravity
    
    def getCalibrationStatus(self):
        return self.BNO055.calibration_status
    
    def saveCalibration(self) -> bool:
        pass
    
    def loadCalibration(self) -> bool:
        # self.BNO055.offsets_accelerometer
        pass

    def update(self) -> None:
        return

    def autoUpdate(self) -> None:
        return
    
    def kill(self) -> None:
        return