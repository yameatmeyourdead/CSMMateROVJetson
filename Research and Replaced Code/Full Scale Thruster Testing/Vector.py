class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.components = (x,y,z)
    
    def setX(self, x):
        self.components[0] = x

    def setY(self, y):
        self.components[1] = y
    
    def setZ(self, z):
        self.components[2] = z

    def getX(self):
        return self.components[0]
    
    def getY(self):
        return self.components[1]
    
    def getZ(self):
        return self.components[2]
    
    def dotProduct(self, vector):
        return self.getX() * vector.getX() + self.getY() * vector.getY() + self.getZ() * vector.getZ()

SQRT2 = 1.4142136

Thruster1 = Vector(0,0,1)
Thruster2 = Vector(SQRT2/2,SQRT2/2,0)
Thruster3 = Vector(SQRT2/2,-SQRT2/2,0)
velocity = Vector(0,1,0)

print("Vector 1 dot product", Thruster1.dotProduct(velocity))
print("Thruster 2 dot product", Thruster2.dotProduct(velocity))
print("Thruster 3 dot product", -Thruster3.dotProduct(velocity))