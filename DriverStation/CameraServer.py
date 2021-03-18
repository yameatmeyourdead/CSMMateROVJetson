import imagezmq
import cv2
from . import Logger
from .CameraGUIDriver import CameraGUIDriver
from multiprocessing import Process, set_start_method, Queue

logger = Logger.LOGGER

def waitForImage(queues):
    # Create the server
    imageHub = imagezmq.ImageHub()

    # TODO REPLACE THIS WITH GUI CODE
    # start looping over all the frames 
    while True:
        # receive client name and frame from the client and acknowledge the receipt
        (clientName, frame) = imageHub.recv_image()

        # if recieved client did not specify camera designation error out
        if(len(clientName) <= 6):
            logger.log("received image did not contain valid camera designation")
            

        # grab camera designation
        cameraDesignation = int(clientName[6:])

        # depending upon camera designation put it in corresponding queue
        for index in range(4):
            if(cameraDesignation == index):
                queues[index].put(frame)

        # cv2.imshow(clientName, frame)
        # cv2.waitKey(1)
        imageHub.send_reply(b'OK') 

class CameraServer:
    def __init__(self):
        '''
        Use to create distinct camera server using imagezmq
        One has already been created for you in /DriverStation/__main__.py
        call .kill() on CameraServer object in order to stop process

        Usage:
                newCameraServerObject = CameraServer()\n
                newCameraServerObject.start()\n
                (  Some time passes  )\n
                newCameraServerObject.kill()\n
                (  Process is no longer running :)  )
        '''
        # Create the queues (to push grabbed frames)
        # cry
        self.queues = [Queue(), Queue(), Queue(), Queue()]

        # punch a baby
        self.guiDriver = CameraGUIDriver(self.queues)
    
    def getGuiDriver(self):
        return self.guiDriver

    def start(self):
        set_start_method('spawn')
        self.cameraServer = Process(target=waitForImage, args=(self.queues))
        self.cameraServer.start()
    
    def kill(self):
        self.cameraServer.kill()