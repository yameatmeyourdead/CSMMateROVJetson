# USE THIS TO CREATE "STATIC" VARIABLES / WHEN YOU WANT JAVA STYLE STATIC CLASSES

from adafruit_servokit import ServoKit
from adafruit_motor import servo
import os
import time
import multiprocessing
import traceback
import numpy
import board
import busio
import adafruit_pca9685

# Creation of EStop Exception and its Fatal counterpart (Fatal EStop completely shuts down computer)
class EStopInterruptFatal(Exception): args: True 
class EStopInterrupt(Exception): ...

# PCA9685 should be connected to jetson on J41 pins 27(SDA)/28(SCL) for Bus0 or pins 3(SDA)/5(SCL) for Bus1 as well as relevant voltage (pin1 3.3v)
# Default I2C address is 0x40
kit = ServoKit(channels=16)

# Constant "dictionary" for PCA9685
# Thrusters
THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
# NOT YET IMPLEMENTED TODO: UNCOMMENT
# THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
# THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
# THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
# THRUSTER_Z_LEFT = kit._items[4] = servo.ContinuousServo(kit._pca.channels[4])
# THRUSTER_Z_FRONT = kit._items[5] = servo.ContinuousServo(kit._pca.channels[5])
# THRUSTER_Z_RIGHT = kit._items[6] = servo.ContinuousServo(kit._pca.channels[6])
# THRUSTER_Z_BACK = kit._items[7] = servo.ContinuousServo(kit._pca.channels[7])
# THRUSTERS = [THRUSTER_FRONT_LEFT,THRUSTER_FRONT_RIGHT,THRUSTER_BACK_LEFT,THRUSTER_BACK_RIGHT,THRUSTER_Z_LEFT,THRUSTER_Z_FRONT,THRUSTER_Z_RIGHT,THRUSTER_Z_BACK]
# Manipulator
MANIP_ELBOW_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[8])
# MANIP_ELBOW_SERVO_2 = kit._items[9] = servo.Servo(kit._pca.channels[9])
MANIP_WRIST_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[10])
MANIP_LEVEL_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[11])
# MANIP_CLAMP_SERVO = kit.servo[12]
# MANIP_SERVOS = [MANIP_ELBOW_SERVO,MANIP_ELBOW_SERVO_2,MANIP_WRIST_SERVO,MANIP_LEVEL_SERVO,MANIP_CLAMP_SERVO]
MANIP_SERVOS = [MANIP_ELBOW_SERVO,MANIP_WRIST_SERVO,MANIP_LEVEL_SERVO]
# MicroROV THIS MAY BE REPLACED BY USB SERVO HUB TODO: IMPLEMENT IF TRUE
# NOT YET IMPLEMENTED TODO: UNCOMMENT
# MICRO_SERVO_0 = kit._items[13] = servo.Servo(kit._pca.channels[13])
# MICRO_SERVO_1 = kit._items[14] = servo.Servo(kit._pca.channels[14])
# MICRO_ESC = kit._items[15] = servo.ContinuousServo(kit._pca.channels[15])
# MICRO_SERVOS = [MICRO_SERVO_0, MICRO_SERVO_1]
# MICRO_ESCS = [MICRO_ESC]

# PLACE ALL MODIFICATIONS TO SPECIFIC CHANNEL'S PULSE WIDTH BELOW
# Manip Servo Mods (Rated pulse width)
MANIP_ELBOW_SERVO.set_pulse_width_range(500,2500)
# NOT YET IMPLEMENTED TODO: UNCOMMENT
# MANIP_ELBOW_SERVO_2.set_pulse_width_range(500,2500)
MANIP_WRIST_SERVO.set_pulse_width_range(500,2500)
MANIP_LEVEL_SERVO.set_pulse_width_range(500,2500)
# NOT YET IMPLEMENTED TODO: UNCOMMENT
# MANIP_CLAMP_SERVO.set_pulse_width_range(500,2500)
# Thruster Mods (Experimentally found pulse width because specs lied to us :) ) 
# (in reality its probably a library thing but i dont want to debug/rewrite ServoKit.continuous_servo :P )
THRUSTER_FRONT_LEFT.set_pulse_width_range(1200,2000)
# NOT YET IMPLEMENTED TODO: UNCOMMENT
# THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
# THRUSTER_BACK_LEFT.set_pulse_width_range(1200,2000)
# THRUSTER_BACK_RIGHT.set_pulse_width_range(1200,2000)
# THRUSTER_Z_LEFT.set_pulse_width_range(1200,2000)
# THRUSTER_Z_FRONT.set_pulse_width_range(1200,2000)
# THRUSTER_Z_RIGHT.set_pulse_width_range(1200,2000)
# THRUSTER_Z_BACK.set_pulse_width_range(1200,2000)


# =======================
# =======================
# =======================
# =======================

# LOGGER IMPLEMENTATION

def log(strin, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str through str(value)
    NOTE: UNDER NO CIRCUMSTANCE USE THE CHARACTER >
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(strin) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def log_debug(feedback_queue, error, name):
    pass

def log_error(feedback_queue, error, name):
    pass

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
    f.write(f"[{currentTime}] Logger Created\n")

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
    return JOYSTICK.l

def getRightStick():
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return JOYSTICK.r

def getLeftTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return JOYSTICK.lt

def getRightTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return JOYSTICK.rt

def getLeftBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return JOYSTICK.l1

def getRightBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return JOYSTICK.r1

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
    return JOYSTICK.check_presses()



# Constructor creates instance of joystick
JOYSTICK = ControllerResource().__enter__()
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
PORT = 6666

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

def startNetworkListener():
    SOC.connect((IP, PORT))
    while True:
        packet = recvPacket(">")
        if(packet.find("ES")):
            raise EStopInterruptFatal
        elif(packet.find("S")):
            raise EStopInterrupt

# TODO: IMPLEMENT
SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# =======================
# =======================
# =======================
# =======================

# Error-Safe Processes
class EtlStepProcess(multiprocessing.Process):

    def __init__(self, feedback_queue):
        multiprocessing.Process.__init__(self)
        self.feedback_queue = feedback_queue

    def log_info(self, message):
        log(message)

    def log_debug(self, message):
        log_debug(self.feedback_queue, message, self.name)

    def log_error(self, err):
        log_error(self.feedback_queue, err, self.name)

    def saferun(self):
        """Method to be run in sub-process; can be overridden in sub-class"""
        if self._target:
            self._target(*self._args, **self._kwargs)

    def run(self):
        try:
            self.saferun()
        except Exception as e:
            self.log_error(e)
            raise e
        return