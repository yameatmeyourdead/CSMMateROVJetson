from enum import Enum

class EventPriority(Enum):
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4

    def __lt__(self, other):
        return self.value > other.value
    
    def __le__(self, other):
        return self.value >= other.value
    
    def __gt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value <= other.value