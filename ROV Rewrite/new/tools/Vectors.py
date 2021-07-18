import math

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
        return ((self.i ** 2) + (self.j ** 2) + (self.k ** 2)) ** .5

    @staticmethod
    def dot(a:'Vector3f', b:'Vector3f') -> float:
        """dot two vectors together"""
        return float(a.i * b.i + a.j * b.j + a.k * b.k)
    
    @staticmethod
    def dotTheta(a:'Vector3f', b:'Vector3f'):
        return (Vector3f.dot(a,b) / (a.getMagnitude() * b.getMagnitude()))
    
    @staticmethod
    def cross(a:'Vector3f', b:'Vector3f') -> 'Vector3f':
        """get the cross product of two vectors, specifically a x b"""
        return Vector3f(a.j*b.k - a.k*b.j, a.k*b.i - a.i*b.k, a.i*b.j - a.j*b.i)

    # overload basic operators (more complex operators do not make sense to implement)
    def __add__(self, o:'Vector3f'):
        return Vector3f(self.i + o.i, self.j + o.j, self.k + o.k)

    def __sub__(self, o:'Vector3f'):
        return Vector3f(self.i - o.i, self.j - o.j, self.k - o.k)
    
    def __mul__(self, o:float):
        return Vector3f(self.i * o, self.j * o, self.k * o)
    
    def __truediv__(self, o:float):
        return Vector3f(self.i / o, self.j / o, self.k / o)
    
    def __floordiv__(self, o:float):
        return Vector3f(self.i // o, self.j // o, self.k // o)
    
    def __pow__(self, o:float):
        return abs((self.i**2 + self.j**2 + self.k**2) ** .5)
    
    def __getitem__(self, item):
        """allow Vector3f to be subscriptable (kinda jank implementation) TODO: literally change data structure lmoa <- annoying and im not going to"""
        return self.__getattribute__(chr(ord('i') + item))
    
    def __str__(self):
        return f"({self.i}, {self.j}, {self.k})"
    
    def __neg__(self):
        return Vector3f(-self.i, -self.j, -self.k)
    def __pos__(self):
        return self

# unneeded
# class Quaternion:
#     """Spatial rotation around fixed point of theta radians about a unit axis (X,Y,Z) that denotes the Euler Axis is given by Quaternion (C, XS, YS, ZS) where C = cos(theta/2) and S = sin(theta/2)"""
#     def __init__(self, S=0, i=0, j=0, k=0) -> None:
#         self.__scalar:float = S
#         self.__vector:Vector3f = Vector3f(i,j,k)
    
#     @classmethod
#     def fromComponents(cls, tupl4):
#         return cls(tupl4[0], tupl4[1], tupl4[2], tupl4[3])
    
#     @classmethod
#     def fromScalarAndVector(cls, scalar:float, vector:Vector3f):
#         return cls(scalar, vector.i, vector.j, vector.k)

#     @classmethod
#     def fromEulerAngles(cls, u, v, w):
#         """does what it says"""
#         # ow
#         return Quaternion(math.cos(u/2) * math.cos(v/2) * math.cos(w/2) + math.sin(u/2) * math.sin(v/2) * math.sin(w/2), math.sin(u/2) * math.cos(v/2) * math.cos(w/2) - math.cos(u/2) * math.sin(v/2) * math.sin(w/2), math.cos(u/2) * math.sin(v/2) * math.cos(w/2) + math.sin(u/2) * math.cos(v/2) * math.sin(w/2), math.cos(u/2) * math.cos(v/2) * math.sin(w/2) - math.sin(u/2) * math.sin(v/2) * math.cos(w/2))

#     @staticmethod
#     def dot(a:"Quaternion", b:"Quaternion"):
#         return(a.__scalar*b.__scalar + Vector3f.dot(a.__vector, b.__vector))
    
#     @staticmethod
#     def dotTheta(a:"Quaternion", b:"Quaternion"):
#         return math.acos(Quaternion.dot(a,b) / (a.norm() * b.norm()))

#     def setComponents(self, S=None, i=None, j=None, k=None):
#         if(S is not None):
#             self.__scalar = S
#         if(i is not None):
#             self.__vector.i = i
#         if(j is not None):
#             self.__vector.j = j
#         if(k is not None):
#             self.__vector.k = k
    
#     def getComponents(self):
#         return (self.__scalar, self.__vector.i, self.__vector.j, self.__vector.k)
    
#     def conjugate(self):
#         """returns conjugate of this quaternion defined as a-bi-cj-dk"""
#         return Quaternion.fromScalarAndVector(self.__scalar, -self.__vector)
    
#     def norm(self) -> float:
#         """Returns ||q||"""
#         return (self.__scalar**2 + self.__vector.i**2 + self.__vector.j**2 + self.__vector.k**2) ** .5
    
#     def versor(self):
#         """Returns unit quaternion of this, called the versor"""
#         return self / self.norm()
    
#     def inverse(self):
#         """computs inverse of this given by q*/|q|^2 == conjugate/norm^2"""
#         return self.conjugate() / (self.norm() ** 2)
    
#     def rotate(self, theta:float, direction:Vector3f):
        
#         return  

#     def __add__(self, o:"Quaternion"):
#         return Quaternion(self.__scalar + o.__scalar, self.__vector.i + o.__vector.i, self.__vector.j + o.__vector.j, self.__vector.k + o.__vector.k)
    
#     def __sub___(self, o:"Quaternion"):
#         return Quaternion(self.__scalar - o.__scalar, self.__vector.i - o.__vector.i, self.__vector.j - o.__vector.j, self.__vector.k - o.__vector.k)
    
#     def __mul__(self, o):
#         """[s_a,a]*[s_b,b] = [s_a * s_b − a ⋅ b, s_a*b + s_b*a + axb]"""
#         if(type(o) == Quaternion):
#             return Quaternion.fromScalarAndVector(self.__scalar * o.__scalar - Vector3f.dot(self.__vector, o.__vector), (o.__vector * self.__scalar) + (self.__vector * o.__scalar) + Vector3f.cross(self.__vector, o.__vector))
#         elif(type(o) == float or int):
#             return Quaternion.fromScalarAndVector(self.__scalar * o, self.__vector * o)
    
#     def __truediv__(self, o:float):
#         return Quaternion.fromScalarAndVector(self.__scalar / o, self.__vector / o)
    
#     def __str__(self):
#         return f"({self.__scalar}, {self.__vector.i}, {self.__vector.j}, {self.__vector.k})"
    
#     def __neg__(self):
#         return Quaternion.fromScalarAndVector(-self.__scalar, -self.__vector)
#     def __pos__(self):
#         return self