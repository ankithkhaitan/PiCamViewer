# Documentation for PiCamViewer

1. **Server (`server.py`):**
    - Listens for incoming connections on a specified IP address and port.
    - Receives video frames sent by the client over a TCP socket.
    - Decodes the received frames and displays them in a window using OpenCV.

2. **Client (`client.py`):**
    - Captures video frames from a webcam using OpenCV.
    - Encodes the frames as JPEG images and sends them to the server over a TCP socket.
    - Displays the captured video locally in a window.

3. **Relation to Computer Networks:**
    - The project demonstrates the use of sockets for communication between two devices over a network.
    - It uses the TCP protocol to ensure reliable transmission of video frames.
    - The client and server communicate using a custom protocol where the size of each frame is sent before the frame data itself.

## How to Run the Code
1. **Install Dependencies:**
    - Ensure Python 3.x is installed on your system.
    - Install the required Python libraries using the following command:
      ```bash
      pip install opencv-python imutils
      ```

2. **Hardware Requirements:**
    - A computer with a webcam for the client.
    - Both the client and server can run on the same machine or different machines connected to the same network.

3. **Running the Server:**
    - Open a terminal and navigate to the directory containing `server.py`.
    - Run the server script:
      ```bash
      python server.py
      ```

4. **Running the Client:**
    - Open a terminal and navigate to the directory containing `client.py`.
    - Run the client script:
      ```bash
      python client.py
      ```
    - A GUI will prompt you to enter the server's IP address and port. By default, it uses `127.0.0.1` (localhost) and port `8485`.

5. **Stopping the Program:**
    - Press the `q` key in the client window to stop the video stream and terminate the client.

## Dependencies
- **Python Libraries:**
  - `socket`: For network communication.
  - `cv2` (OpenCV): For video capture, encoding, decoding, and display.
  - `pickle`: For serializing and deserializing video frames.
  - `struct`: For packing and unpacking binary data.
  - `imutils`: For resizing and flipping video frames.
  - `tkinter`: For creating a simple GUI to input the server's IP and port.

## Notes
- Ensure that the server is running before starting the client.
- If running on different machines, ensure that the server's IP address is accessible from the client machine.
- The video stream may experience latency depending on the network speed and hardware performance.