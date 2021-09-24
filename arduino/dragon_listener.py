import logging
import threading
import traceback
from msvcrt import getch
from multiprocessing.connection import Listener

from serial import SerialException

from arduino_serial import reconnect_arduino
from arduino_serial import ARDUINO
from environment import INTERPROCESS_ADDRESS, TYPE

LOGGER = logging.getLogger(__name__)


def receive_commands_from_dragonfly():    # family is deduced to be 'AF_INET'
    listener = Listener(INTERPROCESS_ADDRESS, authkey=b'secret password')
    LOGGER.info("Listening for connection")

    connection = listener.accept()
    LOGGER.info('connection accepted from', listener.last_accepted)
    while True:
        try:
            message = connection.recv()
            LOGGER.info(f"Dragonfly: {message}")
            ARDUINO.write(message)
        except SerialException as e:
            LOGGER.error("Error listening to Dragon Dictation, Arduino disconnected?")
            LOGGER.error(traceback.format_exc())
            reconnect_arduino()
        except Exception as e:
            LOGGER.error("Error receiving commands from dragonfly")
            LOGGER.error(traceback.format_exc())
            listener.close()
            listener = Listener(INTERPROCESS_ADDRESS, authkey=b'secret password')
            LOGGER.warning("Disconnected, relistening for interprocess connection")
            connection = listener.accept()
            LOGGER.warning("Interprocess reconnected!")


def receive_dictation_from_dragon():
    while True:
        try:
            character = getch()
            LOGGER.info(f"Dragon:    {character}")
            # Arduino is expecting a three byte array of [character, press/release byte, null byte]
            arduino_commands = character + TYPE + b"\x00"
            ARDUINO.write(arduino_commands)
        except Exception as e:
            LOGGER.error("Error listening to Dragon Dictation, Arduino disconnected?")
            LOGGER.error(traceback.format_exc())
            reconnect_arduino()


def main():
    threading.Thread(target=receive_commands_from_dragonfly).start()
    receive_dictation_from_dragon()


if __name__ == "__main__":
    main()
