import os

USE_ARDUINO = os.getenv("USE_ARDUINO", True)
INTERPROCESS_ADDRESS = ('localhost', 6147)
PRESS = b"\x01"
RELEASE = b"\x02"
TYPE = b"\x03"

connection = None
