import cv2
import numpy as np
import socket

# Connect to the server
host = '192.168.1.42'
port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((host, port))
except ConnectionRefusedError:
    print("Connection refused, make sure the server is running.")
    exit()

# Set camera parameters
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    # Resize the frame
    frame = cv2.resize(frame, (640, 480))

    # Encode the frame as JPEG
    _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    # Convert encoded frame to bytes
    data = encoded_frame.tobytes()

    # Send frame size
    client.sendall(len(data).to_bytes(4, 'big'))

    # Send frame data
    client.sendall(data)

# Release the camera and close the connection
cap.release()
client.close()

