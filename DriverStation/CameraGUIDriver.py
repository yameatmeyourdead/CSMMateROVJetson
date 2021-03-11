from multiprocessing import Process, set_start_method, Queue

def updateCams(queues):
    while True:
        index = 0
        for index in range (4):
            if(queues[index].qsize()):
                # Do thing with frame
                frame = queues[index].get()


class CameraGUIDriver:
    
    def __init__(self, que):
        """
        GOD IS DEAD AND I KILLED HIM. NO IM NOT EXPLAINING WHY THIS IS A THING (until i calm down, come read the class comments)
        """
        self.queues = que
    
    def start(self):
        set_start_method("spawn")
        self.guiDriver = Process(target=updateCams)