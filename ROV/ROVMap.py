# USE THIS TO CREATE "STATIC" VARIABLES / WHEN YOU WANT JAVA STYLE STATIC CLASSES

from adafruit_servokit import ServoKit
import os
import time
import numpy
import board
import busio
import adafruit_pca9685

# PCA9685 should be connected to jetson on J41 pins 27(SDA)/28(SCL) for Bus0 or pins 3(SDA)/5(SCL) for Bus1 as well as relevant voltage (pin1 3.3v)
# Default I2C address is 0x40
kit = ServoKit(channels=16)

# Constant dictionary for PCA9685
# "FRONT_LEFT_THRUSTER_ESC": 0, "FRONT_RIGHT_THRUSTER_ESC": 1, "BACK_LEFT_THRUSTER_ESC": 2, "BACK_RIGHT_THRUSTER_ESC": 3 
# "Z_THRUSTER_0_ESC": 4, "Z_THRUSTER_0_ESC": 5, "Z_THRUSTER_0_ESC": 6, "Z_THRUSTER_0_ESC": 7
# "ELBOW_SERVO": 8, "ELBOW_SERVO_2": 9, "WRIST_SERVO": 10, "LEVEL_SERVO": 11,"CLAMP_SERVO": 12
# "MICRO_PLACEHOLDER_SERVO1": 13, "MICRO_PLACEHOLDER_SERVO2": 14, "MICRO_PLACEHOLDER_SERVO3": 15
PCA9685PINOUT = {
    # Thrusters Front Left, Front Rright, Back Left, Back Right, Z Left, Z Front, Z Right, Z Back
    0:[kit.continuous_servo[0], kit.continuous_servo[1], kit.continuous_servo[2], kit.continuous_servo[3], kit.continuous_servo[4], kit.continuous_servo[5], kit.continuous_servo[6], kit.continuous_servo[7]],
    # Manip Servos
    1:[kit.servo[8], kit.servo[9], kit.servo[10], kit.servo[11], kit.servo[12]],
    2:[],
}

# PLACE ALL MODIFICATIONS TO SPECIFIC CHANNEL'S PULSE WIDTH BELOW
# Manip Servo Mods
for servo in PCA9685PINOUT[1]:
    servo.set_pulse_width_range(500,2500)

# =======================
# =======================
# =======================
# =======================

# LOGGER IMPLEMENTATION

def log(strin, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str through str(value)
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(strin) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

currentTime = getTimeFormatted('_')
LOGGER_FILE_PATH = f"ROV/Logs/{currentTime}.txt"
if(os.path.exists(LOGGER_FILE_PATH)):
    os.remove(LOGGER_FILE_PATH)
with open(LOGGER_FILE_PATH, 'w') as f:
    f.write(f"[{currentTime}] Logger Created")

# =======================
# =======================
# =======================
# =======================

# JOYSTICK IMPLEMENTATION

from approxeng.input.selectbinder import ControllerResource
    
def getLeftStick():
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return joystick.l

def getRightStick():
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return joystick.r

def getLeftTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return joystick.lt

def getRightTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return joystick.rt

def getLeftBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return joystick.l1

def getRightBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return joystick.r1

def getDPad():
    """
    Returns list of DPad states indexed as follows  \n
    -> (dleft, dup, dright, ddown)  \n
    val = 1 if pressed else 0  
    """
    buttonStates = getButtonPresses()
    return [buttonStates.dleft, buttonStates.dup, buttonStates.dright, buttonStates.ddown]

def getButtonPresses():
    """
    Returns object of all buttons indexed as follows \n 
    INTUITIVE NAME  ->  STANDARD NAME\n
    x->                 .square     \n
    y->                 .triangle   \n
    b->                 .circle     \n
    a->                 .cross      \n
    Left Stick->        .ls         \n
    Right Stick->       .rs         \n
    View->              .select     \n
    Menu->              .start      \n
    XBox->              .home       \n
    DLeft->             .dleft      \n
    DUp->               .dup        \n
    DRight->            .dright     \n
    DDown->             .ddown      \n
    LBTrigger->         .l1         \n
    LTTrigger->         .l2         \n
    RBTrigger->         .r1         \n
    RTTrigger->         .r2         \n
    To determine if one of these buttons are pressed, use .held(standard name) \n
    returns none if not held otherwise number of seconds held
    """
    return joystick.check_presses()



# Constructor creates instance of joystick
joystick = ControllerResource().__enter__()
# =======================
# =======================
# =======================
# =======================

# NETWORK STUFF!!!!!! (boo)

# Complete Port Map
# 5555 ImageZMQ (look at replacing)
# 6666 Data Transmission Port

import socket
IP = "10.0.0.1"
PORT = "6666"

def sendPacket(data):
    """
    Writes data to socket
    """
    SOC.send(data)

# TODO: Implement support for numpy ndarray
def recvPacket(closer):
    """
    Read data from socket
    Usage recvPacket(">") where > denotes end of data chunk
    Packets received must be denoted as valuable info with data variable closer else they will be thrown away
    e.g. relevantdata(closer) will grab relevant data but relevant(closer)data  or (closer)relevantdata will miss data
    """
    buffer = ""
    while not closer in buffer:
        buffer += SOC.recv(1024)
    
    pos = buffer.find(closer)
    rval = buffer[:pos + len(closer)]
    buffer = buffer[pos + len(closer):]

    return rval

# TODO: Look at this implementation for aforementioned problem
def sendImage(image):
    # Get array 
    SOC.send(image.dumps())

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOC.connect((IP, PORT))

# =======================
# =======================
# =======================
# =======================