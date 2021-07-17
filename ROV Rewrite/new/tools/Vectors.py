class Vector3f:
    def __init__(self, i=0.0, j=0.0, k=0.0) -> None:
        self.i = i
        self.j = j
        self.k = k
    
    @classmethod
    def fromComponents(cls, tupl3):
        cls(tupl3[0], tupl3[1], tupl3[2])
    
    def setComponents(self, tupl3: tuple):
        self.i = tupl3[0]
        self.j = tupl3[1]
        self.k = tupl3[2]
    
    def setComponents(self, i=0.0, j=0.0, k=0.0):
        self.i = i
        self.j = j
        self.k = k

    def getComponents(self):
        """returns 3-tuple of i,j,k components"""
        return (self.i, self.j, self.k)

    def getMagnitude(self):
        return ((self.i ** 2) + (self.j ** 2) + (self.k ** 2)) ** (1/2)

    @staticmethod
    def dot(a:'Vector3f', b:'Vector3f') -> float:
        """dot two vectors together"""
        return float(a.i * b.i + a.j * b.j + a.z * b.z)
    
    @staticmethod
    def cross(a:'Vector3f', b:'Vector3f') -> 'Vector3f':
        """get the cross product of two vectors, specifically a x b"""
        return Vector3f(a.j*b.k - a.k*b.j, a.k*b.i - a.i*b.k, a.i*b.j - a.j*b.i)

    # overload basic operators (more complex operators do not make sense to implement)
    def __add__(self, o:'Vector3f'):
        return Vector3f(self.i + o.i, self.j + o.j, self.z + o.z)

    def __sub__(self, o:'Vector3f'):
        return Vector3f(self.i - o.i, self.j - o.j, self.z - o.z)
    
    def __mul__(self, o:float):
        return Vector3f(self.i * o, )
    
    def __truediv__(self, o:float):
        return Vector3f(self.i / o, self.j / o, self.z / o)
    
    def __floordiv__(self, o:float):
        return Vector3f(self.i // o, self.j // o, self.z // o)
    
    def __pow__(self, o:float):
        return Vector3f(self.i ** o, self.j ** o, self.z ** o)

class Quaternion:
    def __init__(self) -> None:
        pass