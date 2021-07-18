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
    
    def setComponents(self, i=None, j=None, k=None):
        if(i is not None):
            self.i = i
        if(j is not None):
            self.j = j
        if(k is not None):
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
    """Spatial rotation around fixed point of theta radians about a unit axis (X,Y,Z) that denotes the Euler Axis is given by Quaternion (C, XS, YS, ZS) where C = cos(theta/2) and S = sin(theta/2)"""
    def __init__(self, S=0, i=0, j=0, k=0) -> None:
        self.__scalar:float = S
        self.__vector:Vector3f = Vector3f(i,j,k)
    
    @classmethod
    def fromComponents(cls, tupl4):
        return cls(tupl4[0], tupl4[1], tupl4[2], tupl4[3])
    
    def fromScalarVector(cls, scalar:float, vector:Vector3f):
        return cls(scalar, vector.i, vector.j, vector.k)

    def setComponents(self, S=None, i=None, j=None, k=None):
        if(S is not None):
            self.__scalar = S
        if(i is not None):
            self.__vector.i = i
        if(j is not None):
            self.__vector.j = j
        if(k is not None):
            self.__vector.k = k
    
    def getComponents(self):
        return (self.__scalar, self.__vector.i, self.__vector.j, self.__vector.k)
    
    def conjugate(self):
        """returns conjugate of this quaternion defined as a-bi-cj-dk"""
        return Quaternion(self.__scalar, -self.__vector.i, -self.__vector.j, -self.__vector.k)
    
    def norm(self) -> float:
        """Returns ||q||"""
        return (self.__scalar**2 + self.__vector.i**2 + self.__vector.j**2, self.__vector.k**2) ** .5
    
    def versor(self):
        """Returns unit quaternion of this, called the versor"""
        return self / self.norm()

    def __add__(self, o:"Quaternion"):
        return Quaternion(self.__scalar + o.__scalar, self.__vector.i + o.__vector.i, self.__vector.j + o.__vector.j, self.__vector.k + o.__vector.k)
    
    def __sub___(self, o:"Quaternion"):
        return Quaternion(self.__scalar - o.__scalar, self.__vector.i - o.__vector.i, self.__vector.j - o.__vector.j, self.__vector.k - o.__vector.k)
    
    def __mul__(self, o:"Quaternion"):
        """[s_a,a]*[s_b,b] = [s_a * s_b − a ⋅ b, s_a*b + s_b*a + a×b]
        Where """
        return Quaternion.fromScalarVector(self.__scalar * o.__scalar - Vector3f.dot(self.__vector, o.__vector), o.__vector * self.__scalar + self.__vector * o.__scalar + Vector3f.cross(self.__vector, o.__vector)
    
    def __truediv__(self, o:float):
        return Quaternion(self.__scalar / o, self.__vector.i / o, self.__vector.j / o, self.__vector.k / o)