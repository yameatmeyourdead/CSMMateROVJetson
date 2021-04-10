import cv2
import numpy as np
import socket

HOST = '10.0.0.1' # driverstation IP
PORT = 6666 # port to listen to

# create new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # bind our socket to our port
    print("Listening for connections")
    s.listen() # wait for connection
    conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
    with conn:
        print("Connected to", addr) # print who we are connected with
        while True: # while we are connected, read data
            data = conn.recv(1024) # read data sent to port (THIS IS BLOCKING)
            if not data: # if we receive empty byte string, connection has been closed from other end
                break
            # do stuff with data
            conn.sendall(b"ES>") # attempt emergency stop