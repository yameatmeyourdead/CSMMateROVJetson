class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.components = (float(x),float(y),float(z))
        self.magnitude = float(float(x) ** 2 + float(y) ** 2 + float(z) ** 2)
    
    def setX(self, x):
        self.components[0] = x
        self.magnitude = float(float(x) ** 2 + float(self.getY()) ** 2 + float(self.getZ()) ** 2)

    def setY(self, y):
        self.components[1] = y
        self.magnitude = float(float(self.getX()) ** 2 + float(y) ** 2 + float(self.getZ()) ** 2)
    
    def setZ(self, z):
        self.components[2] = z
        self.magnitude = float(float(self.getX()) ** 2 + float(self.getY()) ** 2 + float(z) ** 2)

    def getX(self):
        return self.components[0]
    
    def getY(self):
        return self.components[1]
    
    def getZ(self):
        return self.components[2]
    
    def dotProduct(self, vector):
        return self.getX() * vector.getX() + self.getY() * vector.getY() + self.getZ() * vector.getZ()
    
    def crossProduct(self, vector):
        return Vector((self.getY() * vector.getZ() - self.getZ() * vector.getY()),
                      (self.getZ() * vector.getX() - self.getX() * vector.getZ()),
                      (self.getX() * vector.getY() - self.getY() * vector.getX()))

    def getMagnitude(self):
        return self.magnitude

    def toString(self):
        return self.components

SQRT2 = 1.4142136

if __name__ == "__main__":
    Thruster1 = Vector(0,0,1)
    Thruster2 = Vector(SQRT2/2,SQRT2/2,0)
    Thruster3 = Vector(SQRT2/2,-SQRT2/2,0)
    velocity = Vector(0,1,0)

    print("Vector 1 dot product", Thruster1.dotProduct(velocity))
    print("Thruster 2 dot product", Thruster2.dotProduct(velocity))
    print("Thruster 3 dot product", -Thruster3.dotProduct(velocity))