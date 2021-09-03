import os
from typing import Tuple
from Components import Component
from tools import Logger
import time
import board
import adafruit_bno055

class IMU(Component):
    """Implementation of 9-axis BNO055 IMU and Depth Sensor for Translational/Rotational Velocity Calculations and Rotational Orientation"""
    def __init__(self) -> None:
        self.BNO055 = adafruit_bno055.BNO055_I2C(board.I2C())
        self.calibrate()
    
    def calibrate(self):
        Logger.log("Calibrating IMU, ensure this occured at a time when robot is completely still")
        last = time.time()
        while(not self.BNO055.calibrated):
            if(time.time() - last >= 1):
                results = self.BNO055.calibration_status
                print(f"\n\nSys status: {results[0]}\nGyro status: {results[1]}\nAccel status: {results[2]}\nMagn status: {results[3]}")
            pass
    
    def getTemp(self):
        return self.BNO055.temperature
    
    def getEulerAngles(self):
        return self.BNO055.euler

    def getQuaternion(self):
        return self.BNO055.quaternion
    
    def getGyroscope(self):
        return self.BNO055.gyro

    def getAccelerometer(self):
        return self.BNO055.acceleration

    def getMagnetometer(self):
        return self.BNO055.magnetic

    def getLinearAcceleration(self):
        return self.BNO055.linear_acceleration

    def getGravity(self):
        return self.BNO055.gravity
    
    def getCalibrationStatus(self):
        return self.BNO055.calibration_status
    
    # TODO: FIND OUT HOW THIS WORKS IN THIS LIBRARY
    def saveCalibration(self) -> bool:
        if(self.BNO055.calibrated):
            for componentStatus in self.BNO055.calibration_status:
                if componentStatus != 3:
                    return False
            with open("data\\BNO055_CALIBRATION_DATA.dat", 'w') as f:
                status = (self.BNO055.offsets_accelerometer, self.BNO055.offsets_gyroscope)
                f.write(str(status[0]) + '\n' + str(status[1]))
            return True
        else:
            return False

    # TODO: FIND OUT HOW THIS WORKS IN THIS LIBRARY
    def loadCalibration(self) -> bool:
        if os.path.exists("data\\BNO055_CALIBRATION_DATA.dat"):
            with open("data\\BNO055_CALIBRATION_DATA.dat", 'r') as f:
                CALIBRATION_DATA = f.readlines()
            if(CALIBRATION_DATA is not None):
                self.setSensorOffsets(CALIBRATION_DATA)
            else:
                return False
        else:
            return False
    # TODO: FIND OUT HOW THIS WORKS IN THIS LIBRARY
    # def setSensorOffsets(self, offsets:Tuple[str]):
    #     self.BNO055.offsets_accelerometer = offsets[0].replace('\n', '')
    #     self.BNO055.offsets_gyroscope = offsets[1].replace('\n', '')

    def update(self) -> None:
        return

    def autoUpdate(self) -> None:
        return
    
    def kill(self) -> None:
        return