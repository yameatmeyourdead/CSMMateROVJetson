from abc import ABC, abstractmethod

class Component(ABC):

    # this is a constructor!
    def __init__(self):
        pass

    # Update method for teleoperation
    @abstractmethod
    def Update(self):
        pass

    # Update method for autonomous operation
    @abstractmethod
    def autoUpdate(self):
        pass

    # method for stopping moving components / setting thrust to 0 in preparation for power off / idle
    @abstractmethod
    def kill(self):
        pass
    