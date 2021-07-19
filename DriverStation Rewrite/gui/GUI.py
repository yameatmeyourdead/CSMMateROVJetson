from enum import Enum
from queue import Empty
import tkinter as tk
from tkinter import StringVar, ttk, DoubleVar
import traceback
from PIL import Image, ImageTk
import numpy as np
import cv2
import time
from OpenGL import GL, GLU, GLUT
from OpenGL.GLUT import fonts
from pyopengltk import OpenGLFrame
import psutil
from multiprocessing import Queue

HEIGHT = 720
WIDTH = 1280
DEFAULTBG = '#1e1e1e'
DEFAULTFG = '#ffffff'
DEFAULTBG2 = '#707070'
DEFAULTFONT = ("Arial", 16, "bold")

cameraBuffer = Queue()

varData = {"voltage":0.0, "amperage":0.0, "T0":0.0, "T1":0.0, "T2":0.0, "T3":0.0, "T4":0.0, "T5":0.0, "T6":0.0, "T7":0.0}

rootWindow = tk.Tk(className="\Mines Mate ROV DriverStation", )


def fromRGB(rgb):
    return "#%02x%02x%02x" % rgb   

# define cube
def Cube():
    vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
        )
    GL.glBegin(GL.GL_LINES)
    GL.glColor3f(1,1,1)
    for edge in edges:
        for vertex in edge:
            GL.glVertex3fv(vertices[vertex])
    GL.glEnd()


OFFSET = 0
# def coordinate axes
def CoordAxes():
    # Draw X
    GL.glBegin(GL.GL_LINES)
    GL.glColor3f(1,0,0)
    GL.glVertex3f(-OFFSET, -OFFSET, -OFFSET)
    GL.glVertex3f(1, -OFFSET, -OFFSET)
    GL.glEnd()
    # Draw Y
    GL.glBegin(GL.GL_LINES)
    GL.glColor3f(0,1,0)
    GL.glVertex3f(-OFFSET, -OFFSET, -OFFSET)
    GL.glVertex3f(-OFFSET, 1, -OFFSET)
    GL.glEnd()
    # Draw Z
    GL.glBegin(GL.GL_LINES)
    GL.glColor3f(0,0,1)
    GL.glVertex3f(-OFFSET, -OFFSET, -OFFSET)
    GL.glVertex3f(-OFFSET, -OFFSET, 1)
    GL.glEnd()
    

class orientationFrame(OpenGLFrame):
    def initgl(self):
        GLU.gluPerspective(75, 1, 0.1, 50.0)
        GL.glTranslatef(0.0, 0.0, -5)
        GL.glRotatef(45, 1, 0, 0)
        GL.glRotatef(45, 0, 1, 0)
        CoordAxes()
        self.start = time.time()
        self.nframes = 0
    
    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        # TODO: get quaternion and set rotation of cube to it
        GL.glPushMatrix()
        GL.glRotatef(self.nframes % 360, 0, 1, 0)
        Cube()
        GL.glPopMatrix()

        GL.glPushMatrix()
        CoordAxes()
        GL.glPopMatrix()

        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )


def log(message, tex:tk.Text):
    # dont let console exceed 1 kB
    if(len(tex.get(1.0, tk.END).encode('utf-8')) > 1024):
        tex.delete(1.0, tk.END)
    tex.insert(tk.END, message) # insert message
    tex.see(tk.END) # scroll if necessary

# INITIALIZATION

# start window at WIDTHxHEIGHT and ensure that it cannot resize below these values
rootWindow.geometry(f"{WIDTH}x{HEIGHT}")
rootWindow.minsize(WIDTH, HEIGHT)

# parent background frame drawn as large as window
backgroundFrame = tk.Frame(rootWindow, bg=DEFAULTBG)
backgroundFrame.place(relwidth=1.0, relheight=1.0)

# create frame within rootWindow to allow for camera display
cameraFrame = tk.Frame(backgroundFrame, borderwidth=2, relief="sunken")
cameraFrame.place(relwidth=.6, relheight=.8)

# create camera canvases (image display) and their labels
cameraCanvas0 = tk.Canvas(cameraFrame, bg=DEFAULTBG2, highlightbackground='black', highlightthickness=1)
cameraCanvas0.place(relwidth=.5, relheight=.5)
cameraCanvas0Label = tk.Label(cameraCanvas0, bg=DEFAULTBG2, text="Cam0", borderwidth=1, relief="solid")
cameraCanvas0Label.place(anchor='nw')

cameraCanvas1 = tk.Canvas(cameraFrame, bg=DEFAULTBG2, highlightbackground='black', highlightthickness=1)
cameraCanvas1.place(relx=.5, relwidth=.5, relheight=.5)
cameraCanvas1Label = tk.Label(cameraCanvas1, bg=DEFAULTBG2, text="Cam1", borderwidth=1, relief="solid")
cameraCanvas1Label.place(anchor='nw')

cameraCanvas2 = tk.Canvas(cameraFrame, bg=DEFAULTBG2, highlightbackground='black', highlightthickness=1)
cameraCanvas2.place(rely=.5, relwidth=.5, relheight=.5)
cameraCanvas2Label = tk.Label(cameraCanvas2, bg=DEFAULTBG2, text="Cam2", borderwidth=1, relief="solid")
cameraCanvas2Label.place(anchor='nw')

cameraCanvas3 = tk.Canvas(cameraFrame, bg=DEFAULTBG2, highlightbackground='black', highlightthickness=1)
cameraCanvas3.place(relx=.5, rely=.5, relwidth=.5, relheight=.5)
cameraCanvas3Label = tk.Label(cameraCanvas3, bg=DEFAULTBG2, text="Cam3", borderwidth=1, relief="solid")
cameraCanvas3Label.place(anchor='nw')

cameraCanvases = (cameraCanvas0, cameraCanvas1, cameraCanvas2, cameraCanvas3)

# stupid that i have to make img global but WHATEVER
img = None
def updateCameras():
    try:
        info = cameraBuffer.get_nowait() # camera designation, cv2 image from camera
        global img
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(info[1],(cameraCanvas0.winfo_width(), cameraCanvas0.winfo_height())), cv2.COLOR_BGR2RGB)))
        cameraCanvases[info[0]].create_image(190,144,image=img)
    except Empty:
        pass


# create frame within rootWindow to allow for selection of different operation options
detailFrame = tk.Frame(backgroundFrame, bg=DEFAULTBG, borderwidth=2, relief="sunken")
detailFrame.place(relx=.6, relwidth=.4, relheight=.8)

# create tab controller for detail frame, create default notebook/tab style
tabController = ttk.Notebook(detailFrame)
notebookStyle = ttk.Style()
notebookStyle.theme_use("default")
notebookStyle.configure("TNotebook", background=DEFAULTBG, borderwidth=0)
notebookStyle.configure("TNotebook.Tab", background=DEFAULTBG, foreground=DEFAULTFG, borderwidth=1)
notebookStyle.map("TNotebook.Tab", background=[("selected", DEFAULTBG)])
notebookStyle.map("TNotebook.Tab", expand=[("selected", [1, 1, 1, 0])])
tabStyle = ttk.Style()
tabStyle.configure("TFrame", background=DEFAULTBG, borderwidth=2, relief="sunken")

# drive tab
driveTab = ttk.Frame(tabController)
tabController.add(driveTab, text="Drive")
# orientationCanvas = tk.Canvas(driveTab, background=DEFAULTBG2, width=200, height=200)
# orientationCanvas.pack(side="top", anchor='ne')
orientation = orientationFrame(driveTab, width=200, height=200)
orientation.animate=1
orientation.pack(anchor='ne')


# camera tab
cameraTab = ttk.Frame(tabController)
tabController.add(cameraTab, text="Camera")

# command tab
commandTab = ttk.Frame(tabController)
tabController.add(commandTab, text="Command")


# options tab
optionsTab = ttk.Frame(tabController)
tabController.add(optionsTab, text="Options")

# pack tab controller
tabController.pack(expand=1, fill="both")

# create frame for display of ROV Status at a glance
statusFrame = tk.Frame(backgroundFrame, bg=DEFAULTBG, borderwidth=2, relief="sunken")
statusFrame.place(rely=.8, relwidth=1, relheight=.2)

powerLabelFrame = tk.LabelFrame(statusFrame, bg=DEFAULTBG, foreground=DEFAULTFG, text="Power", borderwidth=2, relief="sunken")
powerLabelFrame.place(relwidth=.3, relheight=1)
eStop = tk.Button(powerLabelFrame, text="Disable", bg=DEFAULTBG, foreground=DEFAULTFG)
voltageVar = DoubleVar(name="voltageTextVar", value=0)
amperageVar = DoubleVar(name="amerageTextVar", value=40)
voltageLabel = tk.Label(powerLabelFrame, bg=DEFAULTBG, foreground=DEFAULTFG, textvariable=voltageVar)
voltageLabel.pack(side="left")
amperageBar = tk.Canvas(powerLabelFrame, height=80, width=20)
amperageBar.pack(side="right", padx=5)

def updateAmperageBar():
    for i in range(int(amperageVar.get())):
        # amperageBar.create_rectangle(0, 80 - i, 20, 80 - i, fill=(int(1 - i/80), int(i/80), 0))
        pass

jetsonLabelFrame = tk.LabelFrame(statusFrame, bg=DEFAULTBG, foreground=DEFAULTFG, text="Jetson Statistics", borderwidth=2, relief="sunken")
jetsonLabelFrame.place(relx=.3, relwidth=.3, relheight=1)
cpuUtilizationLabel = tk.Label(jetsonLabelFrame, text="CPU", bg=DEFAULTBG, foreground=DEFAULTFG, font=DEFAULTFONT)
cpuUtilizationLabel.grid(row=0, column=0)
cpuUtilizationVar = StringVar(name="cpuUtilization")
cpuUtilization = tk.Label(jetsonLabelFrame, bg=DEFAULTBG, foreground=DEFAULTFG, textvariable=cpuUtilizationVar, font=DEFAULTFONT)
cpuUtilization.grid(row=0, column=1)
ramUsageLabel = tk.Label(jetsonLabelFrame, text="RAM", bg=DEFAULTBG, foreground=DEFAULTFG, font=DEFAULTFONT)
ramUsageLabel.grid(row=1, column=0)
ramUsageVar = StringVar(name="ramUsage")
ramUsage = tk.Label(jetsonLabelFrame, bg=DEFAULTBG, foreground=DEFAULTFG, textvariable=ramUsageVar, font=DEFAULTFONT)
ramUsage.grid(row=1, column=1)

class controlStatus(Enum):
    off = "red"
    connecting = "yellow"
    connected = "green"

controllerLabel = tk.Label(jetsonLabelFrame, text="Controller", bg=DEFAULTBG, foreground=DEFAULTFG, font=DEFAULTFONT)
controllerLabel.grid(row=2, column=0)
controllerStatus = tk.Canvas(jetsonLabelFrame, bg="red", width=40, height=20)
controllerStatus.grid(row=2, column=1)

console = tk.Text(statusFrame, background=DEFAULTBG2)
console.place(relx=.61, rely=.1, relwidth=.38, relheight=.8)

# post init stuff
rootWindow.update()
lastCPUCheck = time.time()
lastControllerStatus = controlStatus.off
currentStatus = controlStatus.connected
def updateWidgets():
    global lastCPUCheck, lastControllerStatus
    voltageVar.set(varData["voltage"])
    
    # if second has passed, update CPU/RAM stats
    if(time.time() - lastCPUCheck > 1):
        lastCPUCheck = time.time()
        cpuUtilizationVar.set(str(psutil.cpu_percent()) + " %  @ " + str(psutil.cpu_freq().current / 1000) + " GHz")
        ramUsageVar.set(str(round(psutil.virtual_memory().used / 1000000000, 2)) + "GB / " + str(round(psutil.virtual_memory().total / 1000000000, 2)) + "GB")
    # if controller status has changed, update color accordingly
    if(currentStatus != lastControllerStatus):
        controllerStatus.configure(bg=currentStatus.value)
        lastControllerStatus = currentStatus
    updateCameras()
    updateAmperageBar()