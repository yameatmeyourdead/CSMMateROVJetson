
#use this to create constants/lists of constants for pinout

#Constant dictionary for PCA9685 (e.g key = SERVO1 and value = pinout of the pins responsible) 4 manip 3 micro 
PCA9685PINOUT = {"FRONT_LEFT_THRUSTER_ESC": 0, "FRONT_RIGHT_THRUSTER_ESC": 1, "BACK_LEFT_THRUSTER_ESC": 2, "BACK_RIGHT_THRUSTER_ESC": 3, 
                "MANIP_PLACEHOLDER_SERVO1": 4, "MANIP_PLACEHOLDER_SERVO2": 5, "MANIP_PLACEHOLDER_SERVO3": 6, "MANIP_PLACEHOLDER_SERVO4": 7,
                "MICRO_PLACEHOLDER_SERVO1": 8, "MICRO_PLACEHOLDER_SERVO2": 9, "MICRO_PLACEHOLDER_SERVO3": 10, "MICRO_PLACEHOLDER_DCMOTORESC": 11}
def getPCA9685Pinout(key):
    return PCA9685PINOUT[key]