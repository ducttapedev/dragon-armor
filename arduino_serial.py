import os
import threading

import serial

USE_ARDUINO = os.getenv("USE_ARDUINO", False)
PORT = os.getenv("PORT", "COM3")
COMMUNICATION_RATE = 9600

PRESS = b"\x01"
RELEASE = b"\x02"
TYPE = b"\x03"


def connect_arduino():
    print("Connecting to Arduino")
    arduino = serial.Serial(PORT, COMMUNICATION_RATE, timeout=0.05)

    # This prints any data we receive from the Arduino programing port (not the keyboard port)
    def handle_data(data):
        if data:
            print("arduino = " + str(data))

    def read_from_port():
        while True:
            reading = arduino.readline()
            handle_data(reading)

    thread = threading.Thread(target=read_from_port)
    thread.start()
    print("Arduino connected")
    return arduino


if USE_ARDUINO:
    ARDUINO = connect_arduino()
