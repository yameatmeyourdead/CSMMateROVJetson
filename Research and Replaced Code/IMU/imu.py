from time import sleep
import busio
import board
import adafruit_lsm9ds1
import math
from .Vector import Vector

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

NineAxisSensor.gyro_scale = adafruit_lsm9ds1.GYROSCALE_245DPS
NineAxisSensor.accel_range = adafruit_lsm9ds1.ACCELRANGE_2G
NineAxisSensor.mag_gain = adafruit_lsm9ds1.MAGGAIN_4GAUSS

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

theta = 0
phi = 0

tilt = 0

while True:
    # update accelerometer, magnetometer, and gyroscope values
    
    accel = Vector.tupleToVector(NineAxisSensor.acceleration)
    gyro = Vector.tupleToVector(NineAxisSensor.gyro)
    mag = Vector.tupleToVector(NineAxisSensor.magnetic)
    
    tilt = math.atan(accel.getX()/accel.getZ())

    print(tilt)