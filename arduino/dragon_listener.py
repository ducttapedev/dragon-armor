import threading
import traceback
from msvcrt import getch
from multiprocessing.connection import Listener

import arduino_serial
from arduino_serial import ARDUINO_LOCK, ARDUINO, connect_arduino
from environment import INTERPROCESS_ADDRESS, TYPE


def receive_commands_from_dragonfly():    # family is deduced to be 'AF_INET'
    listener = Listener(INTERPROCESS_ADDRESS, authkey=b'secret password')
    print("Listening for connection")

    connection = listener.accept()
    print('connection accepted from', listener.last_accepted)
    while True:
        try:
            message = connection.recv()
            print(message)
            ARDUINO.write(message)
        except Exception as e:
            print("Error receiving commands from dragonfly")
            print(traceback.format_exc())
            listener.close()
            listener = Listener(INTERPROCESS_ADDRESS, authkey=b'secret password')
            print("Disconnected, reListening for connection")
            connection = listener.accept()


def receive_dictation_from_dragon():
    while True:
        try:
            character = getch()
            print(character)
            # Arduino is expecting a three byte array of [character, press/release byte, null byte]
            arduino_commands = character + TYPE + b"\x00"
            ARDUINO.write(arduino_commands)
        except Exception as e:
            print("Error listening to Dragon Dictation")
            print(traceback.format_exc())
            print("Attempting to reconnect to Arduino")
            while ARDUINO is None:
                try:
                    arduino_serial.ARDUINO = connect_arduino()
                except Exception as e:
                    print("Error reconnecting to Arduino")
                    print(traceback.format_exc())


def main():
    threading.Thread(target=receive_commands_from_dragonfly).start()
    receive_dictation_from_dragon()


if __name__ == "__main__":
    main()
