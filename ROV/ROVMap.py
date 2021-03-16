from .xbox import Joystick
from .Logger import Logger
from adafruit_servokit import ServoKit

#use this to create constants/lists of constants for all needs

LOGGER = Logger()
CONTROLLER = Joystick()

# PCA9685 should be connected to jetson on J41 pins 27(SDA)/28(SCL) for Bus0 or pins 3(SDA)/5(SCL) for Bus1 as well as relevant voltage (pin1/7 i think (CHECK CHECK CHECK))
# Run PCA9685 at v+ = 5V 4A
# Default I2C address is 0x40
# Constant dictionary for PCA9685 (e.g key = SERVO1 and value = pinout of the pins responsible) 4 manip 3 micro 
kit = ServoKit(channels=16)
PCA9685PINOUT = {"FRONT_LEFT_THRUSTER_ESC": 0, "FRONT_RIGHT_THRUSTER_ESC": 1, "BACK_LEFT_THRUSTER_ESC": 2, "BACK_RIGHT_THRUSTER_ESC": 3, 
                "MANIP_PLACEHOLDER_SERVO1": 4, "MANIP_PLACEHOLDER_SERVO2": 5, "MANIP_PLACEHOLDER_SERVO3": 6, "MANIP_PLACEHOLDER_SERVO4": 7,
                "MICRO_PLACEHOLDER_SERVO1": 8, "MICRO_PLACEHOLDER_SERVO2": 9, "MICRO_PLACEHOLDER_SERVO3": 10, "MICRO_PLACEHOLDER_DCMOTORESC": 11}
