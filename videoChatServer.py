import socket
import numpy as np
import cv2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("10.11.205.61", 8000))
server.listen(5)
print("Server listening on port 8000")

client_socket, _ = server.accept()

cv2.namedWindow("Server Video")

while True:
    size_bytes = client_socket.recv(4)
    if not size_bytes:
        break
    size = int.from_bytes(size_bytes, 'big')

    data = bytearray()
    while len(data) < size:
        packet = client_socket.recv(size - len(data))
        if not packet:
            break
        data.extend(packet)

    if not data:
        break

    frame = np.frombuffer(data, dtype=np.uint8)

    frame = cv2.imdecode(frame, 1)

    cv2.imshow("Server Video", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
client_socket.close()

