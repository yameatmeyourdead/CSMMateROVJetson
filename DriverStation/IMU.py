import queue
from vpython import *
from time import *
import numpy as np
import math
from multiprocessing import Process
from .DriverStationMap import dataQueue

scene = canvas()

scene.range=5
scene.background=color.yellow
scene.forward=vector(-1,-1,-1)
 
scene.width=1200
scene.height=1080
 
xarrow=arrow(length=.5, shaftwidth=.1, color=color.red,axis=vector(1,0,0))
yarrow=arrow(length=.5, shaftwidth=.1, color=color.green,axis=vector(0,1,0))
zarrow=arrow(length=.5, shaftwidth=.1, color=color.blue,axis=vector(0,0,1))
 
frontArrow=arrow(length=1.5,shaftwidth=.1,color=color.purple,axis=vector(1,0,0))
upArrow=arrow(length=1.5,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0))
 
ROV=box(length=1,width=1,height=1,opacity=.5,pos=vector(0,0,0,))
def doIMU():
    while (True):
        try:
            roll, pitch, yaw = dataQueue.get_nowait().split(',')
    
            rate(50)
            k=vector(cos(yaw)*cos(pitch), sin(pitch),sin(yaw)*cos(pitch))
            y=vector(0,1,0)
            s=cross(k,y)
            v=cross(s,k)
            vrot=v*cos(roll)+cross(k,v)*sin(roll)
    
            frontArrow.axis=k
            upArrow.axis=vrot
            ROV.axis=k
            ROV.up=vrot

        except queue.Empty:
            pass

IMUManager = Process(target=doIMU)