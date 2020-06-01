#!/usr/bin/python3
import time
import sys
import serial
from flask import Flask, render_template

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

try:
	if __name__ == "__main__":
		serial_port.write(b'0')
		time.sleep(1)
		serial_port.write(b'S')
		time.sleep(1)
		app.run(host='0.0.0.0', port=80, debug=True)
except KeyboardInterrupt:
    pass
except Exception as e:
    print("Error: " + str(e))
finally:
	serial_port.close()