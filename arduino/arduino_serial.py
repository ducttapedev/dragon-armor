import logging
import os
import threading
import traceback
import serial

from serial import SerialException

from environment import USE_ARDUINO

LOGGER = logging.getLogger(__name__)
PORT = os.getenv("PORT", "COM3")
COMMUNICATION_RATE = 9600


def connect_arduino():
    LOGGER.info("Connecting to Arduino")
    arduino = serial.Serial(PORT, COMMUNICATION_RATE, timeout=0.05)

    # This prints any data we receive from the Arduino programing port (not the keyboard port)
    def handle_data(data):
        if data:
            LOGGER.info("arduino = " + str(data))

    def read_from_port():
        while True:
            try:
                reading = arduino.readline()
                handle_data(reading)
            except SerialException as e:
                LOGGER.error("Error reading from Arduino")
                LOGGER.error(traceback.format_exc())
                reconnect_arduino()

    thread = threading.Thread(target=read_from_port)
    thread.start()
    LOGGER.info("Arduino connected")
    return arduino


def reconnect_arduino():
    LOGGER.error("reconnection to Arduino currently not supported (we get access denied error)! restart program")
    exit(0)
    # print("Attempting to reconnect to Arduino")
    # environment.ARDUINO = None
    # while environment.ARDUINO is None:
    #     try:
    #         environment.ARDUINO = connect_arduino()
    #     except Exception as e:
    #         print("Error reconnecting to Arduino")
    #         print(traceback.format_exc())
    # print("Reconnected to Arduino!")


if USE_ARDUINO:
    ARDUINO_LOCK = threading.Lock()
    ARDUINO = connect_arduino()
