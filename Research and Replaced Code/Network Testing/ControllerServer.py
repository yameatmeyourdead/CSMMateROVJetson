import socket
import time

HOST = "127.0.0.1" # loopback ip
PORT = 7777 # port to listen to

# create new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # bind our socket to our port
    print("Listening for connections")
    s.listen() # wait for connection
    conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
    try:
        with conn:
            print("Connected to", addr) # print who we are connected with
            while True: # while we are connected, read data and do something with it
                print(s.recv())
    # connection was reset from other side (or maybe your network dropped)
    except ConnectionResetError:
        print("Connection with", addr, " forcibly closed")