from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))
picam2.start()

while True:
    frame = picam2.capture_array()
    cv2.imshow("Pi Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
