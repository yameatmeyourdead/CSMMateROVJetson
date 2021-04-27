from Vector import Vector
from datetime import datetime
import time
import math
from tkinter import *


def PID(Kp, Ki, Kd, MV_offset=Vector()):
    # initialize stored data
    P = Vector()
    I = Vector()
    D = Vector()
    t_prev = datetime.now().microsecond
    e_prev = Vector() # no error on start

    #Initial Control
    MV = MV_offset

    while True:
        # return calculated variable, wait for new data
        t, PV, SP = yield MV
        
        print(t, t_prev)

        # PID Calculations
        # calculate error
        e = SP - PV
        print(f"Error {e}")

        # change in time/error
        dt = abs(t - t_prev)
        if(dt == 0):
            dt = 10
        print(f"Time Differential {dt}")
        de = e - e_prev

        # update actuator command (order is important)
        P = e * Kp
        print(f"Proportional {P}")
        I = I + e * dt * Ki
        print(f"Integral {I}")
        D = de / dt * Kd
        print(f"Derivative {D}")

        MV = P + I + D + MV_offset
        print(f"Offset {MV_offset}")
        print(f"Actuator Command {MV}")

        # update stored data
        e_prev = e
        t_prev = t

root = Tk()
root.geometry("640x480")
root.resizable(False, False)

KP = DoubleVar()
KI = DoubleVar()
KD = DoubleVar()

KPLabel = Label(root, text="Kp")
KPLabel.grid_configure(row=0, column=0)
KPEntry = Entry(root)
KPEntry.grid_configure(row=0, column=1)
KPEntry.insert(0,"1")

KILabel = Label(root, text="Ki")
KILabel.grid_configure(row=1, column=0)
KIEntry = Entry(root)
KIEntry.grid_configure(row=1, column=1)
KIEntry.insert(0,"1")

KDLabel = Label(root, text="Kd")
KDLabel.grid_configure(row=2, column=0)
KDEntry = Entry(root)
KDEntry.grid_configure(row=2, column=1)
KDEntry.insert(0,"1")

targetLabel = Label(root, text="Target")
targetLabel.grid_configure(row=4, column=0)
targetEntry = Entry(root)
targetEntry.grid_configure(row=4, column=1)
targetEntry.insert(0,"0,0,0")

MVLabel = Label(root, text="Actuator Command")
MVLabel.grid_configure(row=5, column=0)
MVOutput = Entry(root)
MVOutput.grid_configure(row=5, column=1)



CONTROLLER = PID(1, 1, 1)
CONTROLLER.send(None)


target = Vector()
current = Vector()

def update(MV):
    t = datetime.now().microsecond
    time.sleep(1)
    KP.set(float(KPEntry.get()))
    KI.set(float(KIEntry.get()))
    KD.set(float(KDEntry.get()))
    CONTROLLER = PID(KP.get(), KI.get(), KD.get(), MV)
    CONTROLLER.send(None)
    target = Vector.tupleToVector(parseTarget())
    MV = CONTROLLER.send((t,current,target))
    MVOutput.delete(0,END)
    MVOutput.insert(0,MV)


def parseTarget():
    target = targetEntry.get()
    target.replace(' ', '')
    target = target.split(',')
    for i in range(len(target)):
        target[i] = float(target[i])
    return tuple((target[0], target[1], target[2]))

updateButton = Button(text="Update", command=lambda:update(current))
updateButton.grid_configure(row=7, column=4)



while True:
    try:
        root.update()
    except TclError:
        break