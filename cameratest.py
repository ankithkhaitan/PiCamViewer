import cv2

cam = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cam.isOpened():
    print("Cannot open camera")
    exit()

ret, frame = cam.read()

if not ret:
    print("Failed to grab frame")
else:
    print("Frame captured successfully")

cam.release()
