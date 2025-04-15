import cv2
import socket
import struct
import pickle
import imutils
import tkinter as tk
from tkinter import simpledialog


def get_ip_port():
    IP = '127.0.0.1'
    PORT = '8485'
    def submit():
        nonlocal IP, PORT
        IP = ip_entry.get()
        PORT = port_entry.get()
        root.destroy()

    root = tk.Tk()
    root.title("Enter IP and Port")

    tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=5)
    ip_entry = tk.Entry(root)
    ip_entry.insert(0, "127.0.0.1")
    ip_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Port:").grid(row=1, column=0, padx=10, pady=5)
    port_entry = tk.Entry(root)
    port_entry.insert(0, "8485")
    port_entry.grid(row=1, column=1, padx=10, pady=5)

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()
    return IP, PORT

IP,PORT = get_ip_port()


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

cam = cv2.VideoCapture(0)
img_counter = 0

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, width=320)
    frame = cv2.flip(frame,180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(image, 0)
    size = len(data)

    if img_counter%1==0:
        client_socket.sendall(struct.pack(">L", size) + data)
        cv2.imshow('client',frame)
        
    img_counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cam.release()