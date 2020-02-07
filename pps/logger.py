import logging
from logging import handlers
from .config import PPS_CONFIG


class Logger:
    """
    Class used for logging. It uses standard python logging module. All logs are stored to file set in config. Format of
    is also set in config.
    """
    def __init__(self, logger_name):
        file = PPS_CONFIG.DIRECTORY_PATH + PPS_CONFIG.LOG_FILE
        format_to_use = PPS_CONFIG.LOG_FORMAT
        logging.basicConfig(level=logging.DEBUG)
        my_logger = logging.getLogger(logger_name)
        my_logger.propagate = False
        fh = logging.handlers.RotatingFileHandler(file)
        fh.setLevel(logging.INFO)  # no matter what level I set here
        formatter = logging.Formatter(format_to_use)
        fh.setFormatter(formatter)
        my_logger.addHandler(fh)
        my_logger.setLevel(logging.DEBUG)
        self.fh = fh
        self.logger = my_logger

    def debug(self, message: str):
        """
        Log message with debug priority.
        :param message: str message to write to log
        """
        self.logger.debug(message)

    def info(self, message: str):
        """
        Log message with info priority.
        :param message: str message to write to log
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Log message with warning priority.
        :param message: str message to write to log
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Log message with error priority.
        :param message: str message to write to log
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Log message with critical priority.
        :param message: str message to write to log
        """
        self.logger.critical(message)
