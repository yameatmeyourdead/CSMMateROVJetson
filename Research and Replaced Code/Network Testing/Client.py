import socket
import queue
from typing import ByteString

IP = "127.0.0.1"
PORT = 7777

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

