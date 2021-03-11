import imagezmq
import cv2
from multiprocessing import Process, set_start_method, Queue

def waitForImage():
    # Create the server
    imageHub = imagezmq.ImageHub()

    # Create the queues (to push grabbed frames)
    # imageQueueCam1 = Queue()
    # imageQueueCam2 = Queue()
    # imageQueueCam3 = Queue()
    # imageQueueCam4 = Queue()

    # TODO REPLACE THIS WITH GUI CODE
    # start looping over all the frames 
    while True:
        # receive client name and frame from the client and acknowledge
        # the receipt
        (clientName, frame) = imageHub.recv_image()

        
        cv2.imshow(clientName, frame)


        # imageQueue.put((clientName,frame))
        cv2.waitKey(1)
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