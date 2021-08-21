import os
import threading

import serial

from environment import USE_ARDUINO

PORT = os.getenv("PORT", "COM3")
COMMUNICATION_RATE = 9600


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
    ARDUINO_LOCK = threading.Lock()
    ARDUINO = connect_arduino()
