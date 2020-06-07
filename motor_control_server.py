#!/usr/bin/python3
import time
import cv2
import threading
import sys
import serial
from flask import Flask, Response, render_template
from camera_jetson import Camera

GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=960,  #1280,
    display_height=616, #720,
    framerate=21,       #60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

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

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	try:
		serial_port.write(b'0')
		time.sleep(1)
		serial_port.write(b'S')
		time.sleep(1)
		app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
	except KeyboardInterrupt:
		pass
	except Exception as e:
		print("Error: " + str(e))
	finally:
		serial_port.close()
