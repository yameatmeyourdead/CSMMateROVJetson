import cv2
import numpy as np
import socket

HOST = '127.0.0.1' # standard loopback address
PORT = 6666 # Port to listen to

# create new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(HOST, PORT) # bind our socket to our port
    s.listen() # wait for connection
    conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
    with conn:
        print("Connected to", addr) # print who we are connected with
        while True: # while we are connected, read data
            data = conn.recv(1024) # read data sent to port (THIS IS BLOCKING)
            if not data: # if we receive empty byte string, connection has been closed from other end
                print("Connection Closed with", addr)
                break
            conn.sendall(data) # echo data back to sender