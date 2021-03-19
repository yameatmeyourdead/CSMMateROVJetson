import imagezmq
import cv2
from .CameraGUIDriver import CameraGUIDriver
from multiprocessing import Process, set_start_method, Queue


def waitForImage(queues, LOGGER):
    # Create the server
    imageHub = imagezmq.ImageHub()

    # TODO REPLACE THIS WITH GUI CODE
    # start looping over all the frames 
    while True:
        # receive client name and frame from the client and acknowledge the receipt
        (clientName, frame) = imageHub.recv_image()

        # if recieved client did not specify camera designation error out
        if(len(clientName) <= 6 or not(0 <= int(clientName[6:]) <= 3)):
            LOGGER.log("received image did not contain valid camera designation")
            continue
        
        # grab camera designation
        cameraDesignation = int(clientName[6:])
        
        # Uncomment below line for debug ONLY
        # LOGGER.log(f"received image from camera {cameraDesignation}")
        cv2.imshow(clientName, frame)
        cv2.waitKey(1)
        imageHub.send_reply(b'OK')
            

        # depending upon camera designation put it in corresponding queue
        queues[cameraDesignation].put(frame)

        

class CameraServer:
    def __init__(self, logger):
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
        self.LOGGER = logger

    def start(self):
        try:
            set_start_method('spawn', force=True)
        except RuntimeError:
            pass
        self.cameraServer = Process(target=waitForImage, args=((self.queues,self.LOGGER)))
        self.cameraServer.start()

        # spawn GUI Driver
        self.LOGGER.log("GuiDriver Created")
        self.guiDriver = CameraGUIDriver(self.queues, self.LOGGER)
        self.guiDriver.start()
    
    def kill(self):
        self.guiDriver.kill()
        self.cameraServer.kill()