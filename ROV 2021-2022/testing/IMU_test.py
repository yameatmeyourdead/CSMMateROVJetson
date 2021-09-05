import math
from Components.IMU import IMU as _IMU
# IMU/TEMP TEST

IMU = _IMU()

while True:
    quat = IMU.getQuaternion()
    eulr = IMU.getEulerAngles()
    roll = -math.atan2(2*(quat[0]*quat[1] + quat[2]*quat[3]), 1-2*(quat[1]**2 + quat[2]**2))
    pitch = math.asin(2*(quat[0]*quat[2] - quat[3]*quat[1]))
    yaw = -math.atan2(2*(quat[0]*quat[3] + quat[1]*quat[2]), 1-2*(quat[2]**2 + quat[3]**2))-math.pi/2

    print(quat, roll, pitch, yaw, eulr, end='\r')