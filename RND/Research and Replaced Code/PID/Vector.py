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