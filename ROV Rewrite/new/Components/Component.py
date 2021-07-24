from abc import ABC, abstractmethod

class Component(ABC):
    # this is an initializer!
    def __init__(self):
        pass

    @abstractmethod
    def update(self) -> None:
        """Update method for teleoperation"""
        return

    @abstractmethod
    def autoUpdate(self) -> None:
        """Update method for autonomous operation"""
        return

    @abstractmethod
    def kill(self) -> None:
        """Method for stopping moving components / setting thrust to 0 in preparation for power off / idle"""
        return