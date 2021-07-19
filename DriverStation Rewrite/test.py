import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk

cam = cv2.VideoCapture(1)

root = tk.Tk()

bruh = tk.Canvas(root, width=1280, height=720)
bruh.place(relheight=1, relwidth=1)

img=ImageTk.PhotoImage(Image.open("./assets/box.png"))
bruh.create_image(10,10, image=img)

def do():
    while True:
        # bruh.create_image(10,10, anchor="nw", image=ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2RGB))))
        root.update()

do()