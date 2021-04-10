from ROV.ROVMap import EStopInterrupt
import socket
IP = "10.0.0.1"
PORT = 6666

def sendPacket(data):
    """
    Writes data to socket
    """
    SOC.send(data)

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

def startNetworkListener():
    """
    Attempts to connect to IP, PORT  
    
    """
    SOC.connect((IP, PORT))
    while True:
        packet = recvPacket(b">")
        print("Received packet: ", packet)
        if(packet.find(b'XXESF>') != -1):
            SOC.close()
            raise EStopInterrupt
        elif(packet.find(b'XXS>') != -1):
            SOC.close()
            raise EStopInterrupt
    

# creation of socket object
SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# if this module is not run as a script, do not auto start network listener :)
if __name__ == "__main__":
    print("Attempt to start network listener")
    startNetworkListener()