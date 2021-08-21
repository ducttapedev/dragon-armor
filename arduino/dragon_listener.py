import threading
from msvcrt import getch
from multiprocessing.connection import Listener

from arduino_serial import ARDUINO_LOCK, ARDUINO
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
            ARDUINO_LOCK.acquire()
            ARDUINO.write(message)
        except EOFError as e:
            # listener.close()
            print("Reached EOF?")
            # break
        finally:
            ARDUINO_LOCK.release()


def receive_dictation_from_dragon():
    while True:
        try:
            character = getch()
            print(character)
            ARDUINO_LOCK.acquire()
            # Arduino is expecting a three byte array of [character, press/release byte, null byte]
            arduino_commands = character + TYPE + b"\x00"
            ARDUINO.write(arduino_commands)
        finally:
            ARDUINO_LOCK.release()


def main():
    threading.Thread(target=receive_commands_from_dragonfly).start()
    receive_dictation_from_dragon()


if __name__ == "__main__":
    main()
