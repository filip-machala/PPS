import logging


class Logger:
    def __init__(self):
        self.file = "/var/spool/samba/Test.log"
        self.logger = logging.getLogger('PPS')
        self.logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log(self, message):
        self.logger.info(message)
