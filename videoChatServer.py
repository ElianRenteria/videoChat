import socket
import numpy as np
import cv2

# Initialize server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.1.42", 8000))
server.listen(5)
print("Server listening on port 8000")

# Accept connection from a client
client_socket, _ = server.accept()

# Create window for displaying video
cv2.namedWindow("Server Video")

while True:
    # Receive frame size
    size_bytes = client_socket.recv(4)
    if not size_bytes:
        break
    size = int.from_bytes(size_bytes, 'big')

    # Receive frame data
    data = bytearray()
    while len(data) < size:
        packet = client_socket.recv(size - len(data))
        if not packet:
            break
        data.extend(packet)

    if not data:
        break

    # Convert frame data to NumPy array
    frame = np.frombuffer(data, dtype=np.uint8)

    # Decode frame
    frame = cv2.imdecode(frame, 1)

    # Display frame
    cv2.imshow("Server Video", frame)

    # Check for 'Esc' key press to exit
    if cv2.waitKey(1) == 27:
        break

# Close window and connection
cv2.destroyAllWindows()
client_socket.close()

