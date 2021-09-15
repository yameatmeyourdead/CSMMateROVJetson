from EventPriority import EventPriority

class Event:
    def __init__(self, priority:EventPriority=EventPriority.NORMAL) -> None:
        self.priority = priority
    
    def getData(self) -> None:
        return None

    def getPriority(self) -> EventPriority:
        return self.priority
    
    def __lt__(self, other:"Event"):
        return self.priority < other.priority
    
    def __le__(self, other:"Event"):
        return self.priority <= other.priority
    
    def __gt__(self, other:"Event"):
        return self.priority > other.priority
    
    def __ge__(self, other:"Event"):
        return self.priority >= other.priority

    def __eq__(self, other:"Event"):
        return self.priority == other.priority