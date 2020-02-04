import logging
from logging import handlers


class Logger:
    def __init__(self):
        file = "/var/spool/samba/Test.log"
        format_to_use = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.DEBUG)
        my_logger = logging.getLogger("PPS")
        my_logger.propagate = False
        fh = logging.handlers.RotatingFileHandler(file)
        fh.setLevel(logging.INFO)  # no matter what level I set here
        formatter = logging.Formatter(format_to_use)
        fh.setFormatter(formatter)
        my_logger.addHandler(fh)
        my_logger.setLevel(logging.DEBUG)
        self.fh = fh
        self.logger = my_logger

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
