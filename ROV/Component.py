from abc import ABC, abstractmethod

class Component(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def autoUpdate(self):
        pass

    @abstractmethod
    def kill(self):
        pass
    