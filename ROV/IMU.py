import time
import datetime
import busio
import board
import adafruit_bno055
import vpython
from .ROVMap import Vector, sendQueue
import math

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_bno055.BNO055_I2C(i2c)

NineAxisSensor.gyro_mode = adafruit_bno055.GYRO_125_DPS
NineAxisSensor.accel_range = adafruit_bno055.ACCEL_2G
NineAxisSensor.magnet_mode = adafruit_bno055.MAGNET_ACCURACY_MODE

class EulerAngles():
    def __init__(self, roll=0, pitch=0, yaw=0) -> None:
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
    def toString(self):
        return (f"{self.roll},{self.pitch},{self.yaw}")

class Quaternion():
    def __init__(self, w, x, y, z) -> None:
        self.w = w
        self.x = x
        self.y = y
        self.z = z

def toEulerAngles(q) -> EulerAngles:
    toReturn = EulerAngles()

    sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
    toReturn.roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (q.w * q.y - q.z * q.x)
    if(sinp >= 1):
        toReturn.pitch = math.copysign(math.pi / 2, sinp)
    else:
        toReturn.pitch = math.asin(sinp)
    
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    toReturn.yaw = math.atan2(siny_cosp, cosy_cosp)

    return toReturn

def send(angles):
    sendQueue.put(angles)

while True:
    send(toEulerAngles(NineAxisSensor.quaternion()).toString())
