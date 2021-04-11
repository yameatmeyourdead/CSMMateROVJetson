from adafruit_servokit import ServoKit
from adafruit_motor import servo
from . import Controller

kit = ServoKit(channels=16)

# THRUSTER_Z_LEFT = kit._items[4] = servo.ContinuousServo(kit._pca.channels[4])
# THRUSTER_Z_FRONT = kit._items[5] = servo.ContinuousServo(kit._pca.channels[5])
# THRUSTER_Z_RIGHT = kit._items[6] = servo.ContinuousServo(kit._pca.channels[6])
# THRUSTER_Z_BACK = kit._items[7] = servo.ContinuousServo(kit._pca.channels[7])