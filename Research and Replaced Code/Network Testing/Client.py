import socket
IP = "10.0.0.1"
PORT = 6666

def sendPacket(data):
    """
    Writes data to socket
    """
    SOC.send(data)

# TODO: Implement support for numpy ndarray
def recvPacket(closer):
    """
    Read data from socket
    Usage recvPacket(">") where > denotes end of data chunk
    Packets received must be denoted as valuable info with data variable closer else they will be thrown away
    e.g. relevantdata(closer) will grab relevant data but relevant(closer)data  or (closer)relevantdata will miss data
    """
    buffer = ""
    while not closer in buffer:
        buffer += SOC.recv(1024)
    
    pos = buffer.find(closer)
    rval = buffer[:pos + len(closer)]
    buffer = buffer[pos + len(closer):]

    return rval

def sendImage(image):
    # Get array 
    SOC.send(image.dumps())

def startNetworkListener():
    SOC.connect((IP, PORT))
    while True:
        packet = recvPacket(">")
        if(packet.find("ES")):
            print("FATAL INTERRUPT")
            input()
        elif(packet.find("S")):
            print("INTERRUPT")
            input()

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))
    s.sendall(b'Hello World')
    data = s.recv(1024)

print("Received", data)