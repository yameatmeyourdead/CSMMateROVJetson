# USE THIS TO CREATE "STATIC" VARIABLES / WHEN YOU WANT JAVA STYLE STATIC CLASSES

from multiprocessing.context import Process
from typing import ByteString
from adafruit_servokit import ServoKit
from adafruit_motor import servo
import os
import time
import multiprocessing
import math
import queue
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
THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
THRUSTER_Z_0 = kit._items[4] = servo.ContinuousServo(kit._pca.channels[4])
THRUSTER_Z_1 = kit._items[5] = servo.ContinuousServo(kit._pca.channels[5])
THRUSTER_Z_2 = kit._items[6] = servo.ContinuousServo(kit._pca.channels[6])
THRUSTER_Z_3 = kit._items[7] = servo.ContinuousServo(kit._pca.channels[7])



# Manipulator
MANIP_ELBOW_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[8])
# MANIP_ELBOW_SERVO_2 = kit._items[9] = servo.Servo(kit._pca.channels[9])
MANIP_WRIST_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[10])
MANIP_LEVEL_SERVO = kit._items[8] = servo.Servo(kit._pca.channels[11])
# MANIP_CLAMP_SERVO = kit.servo[12]
# MANIP_SERVOS = [MANIP_ELBOW_SERVO,MANIP_ELBOW_SERVO_2,MANIP_WRIST_SERVO,MANIP_LEVEL_SERVO,MANIP_CLAMP_SERVO]
MANIP_SERVOS = [MANIP_ELBOW_SERVO,MANIP_WRIST_SERVO,MANIP_LEVEL_SERVO]
# MicroROV THIS MAY BE REPLACED BY USB SERVO HUB TODO: IMPLEMENT IF TRUE
# NOT YET IMPLEMENTED
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
THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
THRUSTER_BACK_LEFT.set_pulse_width_range(1200,2000)
THRUSTER_BACK_RIGHT.set_pulse_width_range(1200,2000)
THRUSTER_Z_0.set_pulse_width_range(1200,2000)
THRUSTER_Z_1.set_pulse_width_range(1200,2000)
THRUSTER_Z_2.set_pulse_width_range(1200,2000)
THRUSTER_Z_3.set_pulse_width_range(1200,2000)


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

def log_debug(feedback_queue, error, name):
    pass

def log_error(feedback_queue, traceback, name):
    pass

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

currentTime = getTimeFormatted('_')
LOGGER_FILE_PATH = f"ROV/Logs/{currentTime}.txt" # TODO: Consider changing to latest.txt
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

def updateController():
    JOYSTICK.check_presses()

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
    return JOYSTICK.presses



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

sendQueue = queue.Queue()
recvQueue = queue.Queue()
errQueue = queue.Queue()

def sendPacket(data):
    """
    Writes data to socket
    """
    if (not isinstance(data, ByteString)): # if data is not a bytestring, make it so
        data = data.encode()
    SOC.sendall(data) # send bytestring

# TODO: Implement support for numpy ndarray
def doNetworkHandler():
    SOC.connect((IP, PORT))
    SOC.settimeout(2)
    closer = "<"
    buffer = b""
    while True:
        try:
            sendPacket(sendQueue.get(block=True, timeout=2)) # if queue has item, send it. throws queue.Empty error if empty after timeout (2 seconds)
        except queue.Empty:
            pass
        buffer = SOC.recv(1024) # wait for incoming messages for max 2 seconds
        if(buffer): # if incoming message detected, finish gathering message
            while not closer in buffer:
                buffer += SOC.recv(1024)
            # extract the message
            header = buffer[0:4]
            pos = buffer.find(closer)
            rval = buffer[:pos + len(closer)]
            buffer = buffer[pos + len(closer):]
            # classify messages based on header
            # 100 = Fatal interrupt
            # 010 = Interrupt
            # 000 = Message
            if header == b"100":
                errQueue.put(EStopInterruptFatal())
            elif header == b"010":
                errQueue.put(EStopInterrupt())
            elif header == b"000":
                recvQueue.put(rval.decode()) # add message to the recv queue
            
SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
NetworkingProcess = Process(target=doNetworkHandler)

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

# =======================
# =======================
# =======================
# =======================

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.components = [float(x),float(y),float(z)]
        self.magnitude = float(float(x) ** 2 + float(y) ** 2 + float(z) ** 2)
    
    @classmethod
    def unitVector(cls, x=0.0, y=0.0, z=0.0):
        """
        Create new unit vector
        """
        magnitude = x**2 + y**2 + z**2
        return cls(x/magnitude, y/magnitude, z/magnitude)

    def setX(self, x):
        """
        Set X Component
        """
        self.components[0] = x

    def setY(self, y):
        """
        Set Y Component
        """
        self.components[1] = y
    
    def setZ(self, z):
        """
        Set Z Component
        """
        self.components[2] = z

    def getX(self):
        """
        Get X Component
        """
        return self.components[0]
    
    def getY(self):
        """
        Get Y Component
        """
        return self.components[1]
    
    def getZ(self):
        """
        Get Z Component
        """
        return self.components[2]

    def setXYZ(self, tupl):
        """
        Set X,Y,Z components at once
        """
        self.x = tupl[0]
        self.y = tupl[1]
        self.Z = tupl[2]

    def toUnitVector(self):
        """
        Convert Vector to its Unit Vector equivalent
        """
        magnitude = self.getMagnitude()
        if(magnitude == 0):
            return Vector()
        return Vector(self.getX()/magnitude, self.getY()/magnitude, self.getZ()/magnitude)

    def dotProduct(self, vector):
        """
        Get the dot product of this vector * other
        """
        return self.getX() * vector.getX() + self.getY() * vector.getY() + self.getZ() * vector.getZ()
    
    def crossProduct(self, vector):
        """
        Get the cross product of this vector x other
        """
        return Vector((self.getY() * vector.getZ() - self.getZ() * vector.getY()),
                      (self.getZ() * vector.getX() - self.getX() * vector.getZ()),
                      (self.getX() * vector.getY() - self.getY() * vector.getX()))

    def getMagnitude(self):
        """
        Get magnitude of vector
        """
        return (float(self.getX()) ** 2 + float(self.getY()) ** 2 + float(self.getZ()) ** 2)

    def toString(self):
        """
        Returns components as a formatted string [x,y,z]
        """
        return str(self.components)

    # "overloading" functions

    def __str__(self):
        return self.toString()
    
    def __add__(self, vector):
        return Vector(self.getX() + vector.getX(), self.getY() + vector.getY(), self.getZ() + vector.getZ())
    
    def __sub__(self, vector):
        return Vector(self.getX() - vector.getX(), self.getY() - vector.getY(), self.getZ() - vector.getZ())
    
    def __mul__(self, val):
        return Vector(self.getX() * val, self.getY() * val, self.getZ() * val)
    
    def __truediv__(self, val):
        return Vector(self.getX() / val, self.getY() / val, self.getZ() / val)

# Drive constants

# SLOW DOWN MAN
VELOCITY_MOD = .5

SQRT2 = math.sqrt(2)
SQRT05 = math.sqrt(.5)

# azimuthal thruster vectors
THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0)
THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0)
THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)

THRUSTER_FRONT_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_LEFT_THRUST_VECTOR)
THRUSTER_FRONT_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_RIGHT_THRUST_VECTOR)
THRUSTER_BACK_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_LEFT_THRUST_VECTOR)
THRUSTER_BACK_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_RIGHT_THRUST_VECTOR)

# elevation thruster vectors
THRUSTER_Z_0_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_1_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_2_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_3_THRUST_VECTOR = Vector(0, 0, 1)

THRUSTER_Z_0_TORQUE_VECTOR = Vector(-.5, .5, SQRT05).crossProduct(THRUSTER_Z_0_THRUST_VECTOR)
THRUSTER_Z_1_TORQUE_VECTOR = Vector(.5, .5, SQRT05).crossProduct(THRUSTER_Z_1_THRUST_VECTOR)
THRUSTER_Z_2_TORQUE_VECTOR = Vector(-.5, -.5, SQRT05).crossProduct(THRUSTER_Z_2_THRUST_VECTOR)
THRUSTER_Z_3_TORQUE_VECTOR = Vector(.5, -.5, SQRT05).crossProduct(THRUSTER_Z_3_THRUST_VECTOR)