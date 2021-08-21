import threading
from msvcrt import getch
from multiprocessing.connection import Listener

from environment import INTERPROCESS_ADDRESS


def receive_commands_from_dragonfly():    # family is deduced to be 'AF_INET'
    listener = Listener(INTERPROCESS_ADDRESS, authkey=b'secret password')
    print("Listening for connection")

    connection = listener.accept()
    print('connection accepted from', listener.last_accepted)
    while True:
        try:
            message = connection.recv()
            print(message)
        except EOFError as e:
            # listener.close()
            print("Reached EOF?")
            # break


def receive_dictation_from_dragon():
    while True:
        character = getch()
        print(character)


def main():
    threading.Thread(target=receive_commands_from_dragonfly).start()
    receive_dictation_from_dragon()


if __name__ == "__main__":
    main()
