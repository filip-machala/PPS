from config import *
from print_job import PrintJob
import logging


class Logger:
    def __init__(self):
        self.file = "/var/spool/samba/Test.log"

    def write_to_file(self, print_job: PrintJob):
        text_to_write = print_job.time + " " + print_job.printer + " " + print_job.ip + " " + print_job.file
        logging.basicConfig(filename='/var/spool/samba/test2.log', filemode='a', format='%(asctime)s %(message)s',
                            level=logging.DEBUG)
        logging.debug(text_to_write)

        # file = open(self.file, "a+")
        # file.write(text_to_write)
        # file.close()
