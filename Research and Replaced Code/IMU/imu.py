import time
import busio
import board
import adafruit_lsm9ds1
import math

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

NineAxisSensor.gyro_scale = adafruit_lsm9ds1.GYROSCALE_245DPS
NineAxisSensor.accel_range = adafruit_lsm9ds1.ACCELRANGE_2G
NineAxisSensor.mag_gain = adafruit_lsm9ds1.MAGGAIN_4GAUSS

class Quaternion:
    def __init__(self):
        self.__quaternion = [0,0,0,0]
    
    def getW(self):
        return self.__quaternion[0]
    
    def getX(self):
        return self.__quaternion[1]
    
    def getY(self):
        return self.__quaternion[2]
    
    def getZ(self):
        return self.__quaternion[3]

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.components = [float(x),float(y),float(z)]
    
    @classmethod
    def unitVector(cls, x=0.0, y=0.0, z=0.0):
        """
        Create new unit vector
        """
        magnitude = x**2 + y**2 + z**2
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

PI = math.pi
atan = math.atan

thetaA = 0
phiA = 0

thetaGOld = 0
phiGOld = 0
thetaG = 0
phiG = 0

dt = 0
t_old = 0

while True:
    # update accelerometer, magnetometer, and gyroscope values
    
    accel = Vector.tupleToVector(tuple(NineAxisSensor.acceleration))
    gyro = Vector.tupleToVector(tuple(NineAxisSensor.gyro))
    print(gyro)
    mag = Vector.tupleToVector(tuple(NineAxisSensor.magnetic))
    
    thetaA = atan(accel.getX()/accel.getZ()) * 180 / PI
    phiA = atan(accel.getY()/accel.getZ()) * 180 / PI

    dt = time.time_ns()/1000000 - t_old
    thetaG = thetaGOld + gyro.getY() * dt
    phiG = phiGOld + gyro.getX() * dt
    t_old = time.time_ns()/1000000

    thetaGOld = thetaG
    phiGOld = phiG

    print(f"{thetaA:.2f} , {phiA:.2f}")
    print(f"{thetaG:.2f} , {phiG:.2f}")