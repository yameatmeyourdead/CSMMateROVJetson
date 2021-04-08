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

# PLACE ALL MODIFICATIONS TO SPECIFIC CHANNEL'S PULSE WIDTH BELOW
# Manip Servo Mods
kit.servo[4].set_pulse_width_range(500,2500)
kit.servo[5].set_pulse_width_range(500,2500)
kit.servo[6].set_pulse_width_range(500,2500)
kit.servo[7].set_pulse_width_range(500,2500)

# Constant dictionary for PCA9685 (e.g key = SERVO1 and value = pinout of the pins responsible)
PCA9685PINOUT = {"FRONT_LEFT_THRUSTER_ESC": 0, "FRONT_RIGHT_THRUSTER_ESC": 1, "BACK_LEFT_THRUSTER_ESC": 2, "BACK_RIGHT_THRUSTER_ESC": 3, 
                "ELBOW_SERVO": 4, "ELBOW_SERVO_2": 5, "WRIST_SERVO": 6, "LEVEL_SERVO": 7,"CLAMP_SERVO": 8, 
                "MICRO_PLACEHOLDER_SERVO1": 9, "MICRO_PLACEHOLDER_SERVO2": 10, "MICRO_PLACEHOLDER_SERVO3": 11, "MICRO_PLACEHOLDER_DCMOTORESC": 12}

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
    # Get pickle of array and turn it into byte string, then add relevant closer to denote IMAGE
    SOC.send(image.dumps())

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOC.connect((IP, PORT))

# =======================
# =======================
# =======================
# =======================