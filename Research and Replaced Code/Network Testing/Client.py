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
    buffer = b""
    while not closer in buffer:
        buffer += SOC.recv(1024)
    
    pos = buffer.find(closer)
    rval = buffer[:pos + len(closer)]
    buffer = buffer[pos + len(closer):]

    return rval

def sendImage(image):
    # TODO: IMPLEMENT
    SOC.sendall(b"IMAGE_GOES_HERE")

def startNetworkListener():
    SOC.connect((IP, PORT))
    while True:
        packet = recvPacket(b">")
        if(packet.find(b"ES>")):
            print("FATAL INTERRUPT")
            input()
            break
        elif(packet.find(b"S>")):
            print("INTERRUPT")
            input()
            break
    SOC.close()

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Attempt to start network listener")
startNetworkListener()