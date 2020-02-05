#!/bin/env python3
import time
import sys
import subprocess
import os
from subprocess import PIPE, Popen
import getpass
# from pkpgpdls import analyzer
import logging
from logging import handlers
import re

def main():
    FILE = sys.argv[1]
    # file_to_read = "/var/spool/samba/" + FILE
    # cmd = "pkpgcounter"
    # print(file_to_read)
    # p = subprocess.getoutput(cmd + " <" + file_to_read)
    # print(p)
    tmp = "Ou jet"
    file = open("/var/spool/samba/log.txt", "w")
    file.write(tmp)
    # file.write(stderr)

    # print_file = sys.argv[1]
    # file_to_print = "/var/spool/samba/" + print_file
    # print(file_to_print)
    # subprocess.run(["lpr", "-P HP_LaserJet_P2055dn", file_to_print])

    # Send to printer
    # os.system("lpr -P HP_LaserJet_P2055dn " + file_to_print)

    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler('./logtest.log', maxBytes=10240, backupCount=5)
    fh.setLevel(logging.INFO)  # no matter what level I set here
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('INFO')
    logger.error('ERROR')

    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

#
# def get_file_name(file_name):
#     file = open(file_name, encoding='utf-8')
#     with open(file_name, 'rb') as fh:
#         radek = fh.readline().decode('utf-8')
#         slova = radek.split()
#         while slova[1] != 'ENTER':
#             radek = fh.readline().decode('utf-8')
#             slova = radek.split()
#             if 'JOBNAME' in radek:
#                 x = re.search("JOBNAME=.*", radek)
#                 name = x.group(0).split('=')[1]
#                 return name
#

if __name__ == '__main__':
    main()

