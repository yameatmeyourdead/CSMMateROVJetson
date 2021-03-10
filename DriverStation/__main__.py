# Code for Driver Station (Raspi running PiOS/CentOS/Ubuntu)

#Consider using tkinter????
# from dearpygui.core import *
# from dearpygui.simple import *

# def save_callback(sender, data):
#     print("Save Clicked")

# with window("Example Window"):
#     add_text("Hello, world")
#     add_button("Save", callback=save_callback)
#     add_input_text("string", default_value="Quick brown fox")
#     add_slider_float("float", default_value=0.273, max_value=10)

# start_dearpygui()

# THIS IS WORKING
from .CameraServer import CameraServer

cameraServer = CameraServer()

cameraServer.start()
input("Press to stop")
cameraServer.kill()