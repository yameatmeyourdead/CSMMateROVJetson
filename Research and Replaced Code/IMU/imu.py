from time import sleep
import busio
import board
import adafruit_lsm9ds1
from.Vector import Vector

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

class Quaternion:
    def __init__(self):
        self.__quaternion = [0,0,0,0]
    
    def getW(self):
        return self.__quaternion[0]
    
    def getX(self):
        return self.__quaternion[1]
    
    def getY(self):
        return self.__quaternion[2]
    
    def getZ(self):
        return self.__quaternion[3]

while True:
    # update accelerometer, magnetometer, and gyroscope values
    
    accel = Vector.tupleToVector(NineAxisSensor.acceleration)
    gyro = Vector.tupleToVector(NineAxisSensor.gyro)
    