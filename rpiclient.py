import cv2
import socket
import struct
import pickle
import imutils
import tkinter as tk
from picamera2 import Picamera2


def get_ip_port():
    IP = '100.94.21.11'
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
    ip_entry.insert(0, "100.94.21.11")
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


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, int(PORT)))
    print(f"Connected to server at {IP}:{PORT}")
except Exception as e:
    print(f"Failed to connect to server: {e}")
    exit(1)

try:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": 'BGR888', "size": (320, 240)})
    picam2.configure(config)
    picam2.start()

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    img_counter = 0
    while True:
        print(f"Checkpoint: Starting loop iteration {img_counter}")
        try:
            frame = picam2.capture_array()
            print("Checkpoint: Frame captured")
            frame = cv2.flip(frame, 0)  # Flip vertically to match the original behavior
            print("Checkpoint: Frame flipped")
            result, image = cv2.imencode('.jpg', frame, encode_param)
            print("Checkpoint: Frame encoded")
            data = pickle.dumps(image, 0)
            print("Checkpoint: Frame serialized")
            size = len(data)
            print(f"Checkpoint: Data size calculated - {size} bytes")

            client_socket.sendall(struct.pack(">L", size) + data)
            print("Checkpoint: Data sent to server")
            cv2.imshow('client', frame)
            print("Checkpoint: Frame displayed")
        except Exception as e:
            print(f"Error sending data: {e}")
            break

        img_counter += 1
        print(f"Checkpoint: Incremented img_counter to {img_counter}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Checkpoint: 'q' key pressed, exiting loop")
            break