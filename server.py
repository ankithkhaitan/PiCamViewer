import socket
import cv2
import pickle
import struct
import threading

HOST = '0.0.0.0'
PORT_VIDEO = 8485
PORT_CHAT = 8486

video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind((HOST, PORT_VIDEO))
video_socket.listen(10)
print('Video socket listening on port', PORT_VIDEO)

chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_socket.bind((HOST, PORT_CHAT))
chat_socket.listen(10)
print('Chat socket listening on port', PORT_CHAT)

conn_video, addr_video = video_socket.accept()
conn_chat, addr_chat = chat_socket.accept()
print(f"Connection established with {addr_video} for video and {addr_chat} for chat")

def handle_chat():
    while True:
        try:
            message = conn_chat.recv(1024).decode()
            if message:
                print(f"Client: {message}")
                response = input("You: ")
                conn_chat.sendall(response.encode())
        except:
            print("Chat connection closed.")
            break

chat_thread = threading.Thread(target=handle_chat)
chat_thread.start()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

while True:
    while len(data) < payload_size:
        data += conn_video.recv(4096)
        if not data:
            cv2.destroyAllWindows()
            conn_video, addr_video = video_socket.accept()
            continue
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn_video.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow('server', frame)
    cv2.waitKey(1)