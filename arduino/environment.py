import logging
import os
import sys
from datetime import datetime

USE_ARDUINO = os.getenv("USE_ARDUINO", True)
INTERPROCESS_ADDRESS = ('localhost', 6147)
PRESS = b"\x01"
RELEASE = b"\x02"
TYPE = b"\x03"

LOGGING_FORMAT = u"[%(levelname)-7s] %(asctime)s %(threadName)s [%(filename)s:%(lineno)d] %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# ROOT_PATH = os.path.expanduser('~') + ""
ROOT_PATH = "C:/Users/User/PycharmProjects/dragon-armor"
SCRIPT_NAME = sys.argv[0].split("/")[-1].split("\\")[-1].split(".")[0]
LOGGING_FILE_NAME_BASE = f"{ROOT_PATH}/logs/" + SCRIPT_NAME + "/{:%Y-%m/%d/%H/%M-%S}".format(datetime.now())
LOGGING_ERROR_FILE = f"{ROOT_PATH}/logs/" + SCRIPT_NAME + "/{:%Y-%m/%d}_ERROR.log".format(datetime.now())

connection = None


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    terminal_format = logging.Formatter(LOGGING_FORMAT)
    terminal_handler = logging.StreamHandler(sys.stdout)
    terminal_logging_level = getattr(logging, LOG_LEVEL)
    print(f"Logging to terminal with log level {LOG_LEVEL}")
    terminal_handler.setLevel(terminal_logging_level)
    terminal_handler.setFormatter(terminal_format)
    logger.addHandler(terminal_handler)

    for logging_level in ("DEBUG", "INFO", "WARNING", "ERROR"):
        file_formatter = logging.Formatter(LOGGING_FORMAT)
        logging_filename = LOGGING_ERROR_FILE if logging_level == "ERROR" else\
            LOGGING_FILE_NAME_BASE + f"_{logging_level}.log"
        try:
            os.makedirs(os.path.dirname(logging_filename), exist_ok=True)
            file_handler = logging.FileHandler(logging_filename, mode="a", encoding="UTF-8")
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(logging_level)
            logger.addHandler(file_handler)
            print(f"Logging {logging_level} to file {logging_filename}")
        except Exception as e:
            logger.error(f"Could not make folders for {logging_filename}, disabling log to file")
            logger.exception(e)
    return logging.getLogger(__name__)


LOGGER = create_logger()
