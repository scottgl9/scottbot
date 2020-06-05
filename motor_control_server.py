#!/usr/bin/python3
import time
import cv2
import threading
import sys
import serial
from flask import Flask, Response, render_template

global video_frame
video_frame = None

global thread_lock
thread_lock = threading.Lock()

GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

app = Flask(__name__)

serial_port = serial.Serial(
    port="/dev/ttyACM0",#"/dev/ttyTHS1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

def robot_stop():
    serial_port.write(b'S')
	#time.sleep(1)

def robot_forward():
	serial_port.write(b'F')

def robot_backward():
	serial_port.write(b'B')

def robot_turn_left():
	serial_port.write(b'L')

def robot_turn_right():
	serial_port.write(b'R')

@app.route("/")
def getPage():
	templateData = {
		'title' : 'Robot Motor Controller'
	}
	return render_template('index.html', **templateData)

@app.route("/stop", methods=['GET', 'POST'])
def stop():
	robot_stop()
	return ('', 204)

@app.route("/forward", methods=['GET', 'POST'])
def forward():
	robot_forward()
	return ('', 204)

@app.route("/backward", methods=['GET', 'POST'])
def backward():
	robot_backward()
	return ('', 204)

@app.route("/turnleft", methods=['GET', 'POST'])
def turn_left():
	robot_turn_left()
	return ('', 204)

@app.route("/turnright", methods=['GET', 'POST'])
def turn_right():
	robot_turn_right()
	return ('', 204)

def captureFrames():
    global video_frame, thread_lock

    # Video capturing from OpenCV
    video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)

    while True and video_capture.isOpened():
        return_key, frame = video_capture.read()
        if not return_key:
            break

        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            video_frame = frame.copy()

        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    video_capture.release()

def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            return_key, encoded_image = cv2.imencode(".jpg", video_frame)
            if not return_key:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encoded_image) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
	try:
		serial_port.write(b'0')
		time.sleep(1)
		serial_port.write(b'S')
		time.sleep(1)
		# Create a thread and attach the method that captures the image frames, to it
		process_thread = threading.Thread(target=captureFrames)
		process_thread.daemon = True
		# Start the thread
		process_thread.start()
		app.run(host='0.0.0.0', port=80, debug=True)
	except KeyboardInterrupt:
		pass
	except Exception as e:
		print("Error: " + str(e))
	finally:
		serial_port.close()
