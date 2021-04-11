from adafruit_servokit import ServoKit
from adafruit_motor import servo
from . import Controller

kit = ServoKit(channels=16)

THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
