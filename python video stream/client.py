import io
import socket
import struct
import time
import cv2

client_socket = socket.socket()

client_socket.connect(('', 8000))  # ADD IP HERE

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    # create the camera capture
    camera = cv2.VideoCapture(0)
    # limit the buffer so we get the newest possible frame
    cv2.CAP_PROP_BUFFERSIZE = 

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 60:
            break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
