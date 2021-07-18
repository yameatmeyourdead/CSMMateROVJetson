import math
import time
import board
from tools.Vectors import Vector3f, Quaternion
import adafruit_bno055
# IMU/TEMP TEST

i2c = board.I2C()
IMU = adafruit_bno055.BNO055_I2C(i2c)
last_val = 0xFFFF

while True:
    rotation = IMU.quaternion

    roll = -math.atan2(2*(rotation[0]*rotation[1] + rotation[2]*rotation[3]), 1-2*(rotation[1]**2 + rotation[2]**2))
    pitch = math.asin(2*(rotation[0]*rotation[2] - rotation[3]*rotation[1]))
    yaw = -math.atan2(2*(rotation[0]*rotation[3] + rotation[1]*rotation[2]), 1-2*(rotation[2]**2 + rotation[3]**2))-math.pi/2

    print(roll , pitch, yaw)