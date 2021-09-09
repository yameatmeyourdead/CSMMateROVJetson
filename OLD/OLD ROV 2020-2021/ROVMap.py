# USE THIS TO CREATE "STATIC" VARIABLES / WHEN YOU WANT JAVA STYLE STATIC CLASSES

from adafruit_servokit import ServoKit
import adafruit_pca9685
from adafruit_motor import servo, stepper
import board, busio
import os
import time
import math
import queue
import traceback

# Creation of EStop Exception and its Fatal counterpart (Fatal EStop completely shuts down computer)
class EStopInterruptFatal(Exception): args: True 
class EStopInterrupt(Exception): ...

# PCA9685 should be connected to jetson on J41 pins 27(SDA)/28(SCL) for Bus0 or pins 3(SDA)/5(SCL) for Bus1 as well as relevant voltage (pin1 3.3v)
# Default I2C address is 0x40
kit = ServoKit(channels=16)
# i2c = busio.I2C(board.SCL, board.SDA) # definition of second PCA9685 (used for stepper motor)
# kit2 = adafruit_pca9685.PCA9685(i2c, address=0x41)
# kit2.frequency = 1600

# Constant "dictionary" for PCA9685
# Thrusters
# THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
# THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
# THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
# THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
# THRUSTER_Z_0 = kit._items[4] = servo.ContinuousServo(kit._pca.channels[4])
# THRUSTER_Z_1 = kit._items[5] = servo.ContinuousServo(kit._pca.channels[5])
# THRUSTER_Z_2 = kit._items[6] = servo.ContinuousServo(kit._pca.channels[6])
# THRUSTER_Z_3 = kit._items[7] = servo.ContinuousServo(kit._pca.channels[7])
# THRUSTERS = [THRUSTER_FRONT_LEFT, THRUSTER_FRONT_RIGHT, THRUSTER_BACK_LEFT, THRUSTER_BACK_RIGHT, THRUSTER_Z_0, THRUSTER_Z_1, THRUSTER_Z_2, THRUSTER_Z_3]

# Manipulator
MANIP_ELBOW_SERVO_2 = kit._items[8] = servo.Servo(kit._pca.channels[8])
MANIP_ELBOW_SERVO = kit._items[9] = servo.Servo(kit._pca.channels[9])
MANIP_WRIST_SERVO = kit._items[10] = servo.Servo(kit._pca.channels[10])
MANIP_LEVEL_SERVO = kit._items[11] = servo.Servo(kit._pca.channels[11])
MANIP_CLAMP_SERVO = kit._items[12] = servo.Servo(kit._pca.channels[12])
MANIP_SERVOS = [MANIP_ELBOW_SERVO,MANIP_ELBOW_SERVO_2,MANIP_WRIST_SERVO,MANIP_LEVEL_SERVO,MANIP_CLAMP_SERVO]

#Micro Rov

# MICROROV_WINCH = kit._items[13] = servo.ContinuousServo(kit._pca.channels[13])

# Stepper motor (OBSOLETE??)
# pwma = kit2.channels[8]
# ain1 = kit2.channels[10]
# ain2 = kit2.channels[9]

# pwmb = kit2.channels[13]
# bin1 = kit2.channels[11]
# bin2 = kit2.channels[12]
# MICROROV_WINCH = stepper.StepperMotor(ain1, ain2, bin1, bin2)
# # hold pins high for TB6612 driver
# pwma.duty_cycle = 0xffff
# pwmb.duty_cycle = 0xffff

# MICROROVCOMPORT = "COM4" # windows (my computer assigned it to COM4 yours might not (this program shouldnt be run on a windows os but whatev))
MICROROVCOMPORT = "/dev/ttyACM0" # linux ACM0 subject to change depending upon accessories plugged into the computer o_o TODO: figure out how this works

# Manip Servo Mods (Rated pulse width)
MANIP_ELBOW_SERVO.set_pulse_width_range(500,2500)
MANIP_ELBOW_SERVO_2.set_pulse_width_range(500,2500)
MANIP_WRIST_SERVO.set_pulse_width_range(600,2400)
MANIP_LEVEL_SERVO.set_pulse_width_range(500,2500)
MANIP_CLAMP_SERVO.set_pulse_width_range(500,2500)

# Thruster Mods (Experimentally found pulse width because specs lied to us :) (1100->1900 base)) 
# (in reality its probably a library thing but i dont want to debug/rewrite ServoKit.continuous_servo :P )
# THRUSTER_FRONT_LEFT.set_pulse_width_range(1200,2000)
# THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
# THRUSTER_BACK_LEFT.set_pulse_width_range(1200,2000)
# THRUSTER_BACK_RIGHT.set_pulse_width_range(1200,2000)
# THRUSTER_Z_0.set_pulse_width_range(1200,2000)
# THRUSTER_Z_1.set_pulse_width_range(1200,2000)
# THRUSTER_Z_2.set_pulse_width_range(1200,2000)
# THRUSTER_Z_3.set_pulse_width_range(1200,2000)

# =======================
# =======================
# =======================
# =======================

# LOGGER IMPLEMENTATION

def log(data, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(data) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

LOGGER_FILE_PATH = "/home/mines-mate-rov/CSMMateROVJetson/ROV/Logs/latest.txt"
if(os.path.exists(LOGGER_FILE_PATH)):
    if(os.path.exists("/home/mines-mate-rov/CSMMateROVJetson/ROV/Logs/last.txt")):
        os.remove("/home/mines-mate-rov/CSMMateROVJetson/ROV/Logs/last.txt")
    os.rename(LOGGER_FILE_PATH, "/home/mines-mate-rov/CSMMateROVJetson/ROV/Logs/last.txt")
with open(LOGGER_FILE_PATH, 'w') as f:
    f.write(f"[{getTimeFormatted(':')}] Logger Created\n")

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
# Todo: replace with asyncio implementation (will probably be slightly cleaner)

import socket
import _thread
import time
import queue
from multiprocessing import Process

IP = "10.0.0.2" # Jetson IP
CLIENT = "10.0.0.1" # IP of Driver Station
# use different ports to ensure they are always available for binding
SENDPORT = 6667
RECVPORT = 6666

# queues to handle different data (allows for communication between processes and threads)
errQueue = queue.Queue()
dataQueue = queue.Queue()

sendQueue = queue.Queue()

def server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    while True:
        _thread.start_new_thread(handle_connection, server.accept())

def handle_connection(client, address):
    """Data MUST be structured like this  
    000< for EStopInterrupt
    001< for Interrupt
    010(data)< for all other data"""
    client.settimeout(0.1)
    data = recvall(client)
    data = data.decode()
    if(data == ""): # error check
        client.shutdown(socket.SHUT_RD)
        client.close()
        return
    tod = data[0:3] # type of data header
    if(tod == "000"):
        errQueue.put("InterruptFatal")
    elif(tod == "001"):
        errQueue.put("Interrupt")
    elif(tod == "010"):
        dataQueue.put(data[4:])
    client.shutdown(socket.SHUT_RD)
    client.close()

def recvall(connection):
    """Receive all data from socket and return it as bytestring"""
    buffer = b""
    while "<" not in buffer:
        try:
            buffer += connection.recv(1024)
        except socket.timeout:
            pass
    try:
        toReturn = buffer[:buffer.index('<')]
    except ValueError:
        toReturn = b""
    finally:
        return toReturn

def client(host, port):
    """If item exists in sendQueue, it will get sent"""
    while True:
        try:
            time.sleep(.001)
            data = sendQueue.get(block=False)
        except queue.Empty:
            continue
        else:
            doClientConnection(data, host, port)

def doClientConnection(data, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        time.sleep(0.1) # wait for thread to display connection
        # send all data
        s.sendall(data.encode() + b"<")

def startJetsonNetworking():
    _thread.start_new_thread(server, ("", RECVPORT))
    client(CLIENT, SENDPORT)

JetsonNetworking = Process(target=startJetsonNetworking) # two threaded process (one child)

# =======================
# =======================
# =======================
# =======================

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.components = [float(x),float(y),float(z)]
    
    @classmethod
    def unitVector(cls, x=0.0, y=0.0, z=0.0):
        """
        Create new unit vector
        """
        magnitude = (x**2 + y**2 + z**2) ** .5
        if(magnitude == 0):
            return Vector()
        return cls(x/magnitude, y/magnitude, z/magnitude)
    
    @classmethod
    def tupleToVector(cls, tupl):
        return cls(tupl[0], tupl[1], tupl[2])

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
        return (float(self.getX()) ** 2 + float(self.getY()) ** 2 + float(self.getZ()) ** 2) ** .5

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