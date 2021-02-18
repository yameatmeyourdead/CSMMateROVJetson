from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def autoUpdate(self):
        pass

    @abstractmethod
    def kill(self):
        pass
    