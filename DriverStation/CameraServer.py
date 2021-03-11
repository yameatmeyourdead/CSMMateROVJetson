import imagezmq
import cv2
from . import DriverStationMap
from .CameraGUIDriver import CameraGUIDriver
from multiprocessing import Process, set_start_method, Queue

logger = DriverStationMap.LOGGER

def waitForImage():
    # Create the server
    imageHub = imagezmq.ImageHub()

    # Create the queues (to push grabbed frames)
    imageQueueCam1 = Queue()
    imageQueueCam2 = Queue()
    imageQueueCam3 = Queue()
    imageQueueCam4 = Queue()

    # cry
    queues = [imageQueueCam1, imageQueueCam2, imageQueueCam3, imageQueueCam4]

    # punch a baby
    guiDriver = CameraGUIDriver(queues)

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
        pass
    
    def start(self):
        set_start_method('spawn')
        self.cameraServer = Process(target=waitForImage)
        self.cameraServer.start()
    
    def kill(self):
        self.cameraServer.kill()    