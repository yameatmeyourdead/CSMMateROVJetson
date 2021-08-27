

class Quaternion:
    def __init__(self, i=0.0, j=0.0, k=0.0, w=0.0) -> None:
        self._i:float = i
        self._j:float = j
        self._k:float = k
        self._w:float = w
    
    def getI(self):
        return self._i
    
    def setI(self, i):
        self._i = i
    
    def getJ(self):
        return self._j
    
    def setJ(self, j):
        self._j = j
    
    def getK(self):
        return self._k
    
    def setK(self, k):
        self._k = k
    
    def getW(self):
        return self._w

    def setW(self, w):
        self._w = w
    
    def toTuple(self):
        return (self._i, self._j, self._k, self._w)

    def __setitem__(self, item, val):
        if(item == 0):
            self._i = val
        elif(item == 1):
            self._j = val
        elif(item == 2):
            self._k = val
        elif(item == 3):
            self._w = val

    def __getitem__(self, item):
        if(item == 0):
            return self._i
        elif(item == 1):
            return self._j
        elif(item == 2):
            return self._k
        elif(item == 3):
            return self._w

    def __str__(self):
        return f"({self._i}, {self._j}, {self._k}, {self._w})"
    
    def __repr__(self):
        return str(self)