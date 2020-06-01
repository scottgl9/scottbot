#!/usr/bin/python3
import time
import sys
import serial

serial_port = serial.Serial(
    port="/dev/ttyACM0",#"/dev/ttyTHS1",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

time.sleep(1)

try:
    # Send a simple header
    #serial_port.write("TFFF1".encode())
    serial_port.write(b'0')
    time.sleep(1)
    serial_port.write(b'F')
    time.sleep(1)
    serial_port.write(b'S')
    time.sleep(1)
    serial_port.write(b'B')
    time.sleep(1)
    serial_port.write(b'S')
    time.sleep(1)
    serial_port.write(b'L')
    time.sleep(1)
    serial_port.write(b'S')
    time.sleep(1)
    serial_port.write(b'R')
    time.sleep(1)
    serial_port.write(b'S')
    while True:
        if serial_port.inWaiting() > 0:
            data = serial_port.read()
            print(data)
            break

except KeyboardInterrupt:
    pass

except Exception as e:
    print("Error: " + str(e))

finally:
    serial_port.close()
    pass
