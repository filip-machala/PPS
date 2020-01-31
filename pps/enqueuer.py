#!/bin/env python3
from redis import Redis
from rq import Queue
# from print_job import PrintJob
from logic import handle_print_job
import sys
from pps import logger
import time
from getpass import getuser
import logging
import logging.handlers
import re
import os
import subprocess


def main():
    # TODO check arguments exists
    file = sys.argv[1]
    ip = sys.argv[2]
    printer = sys.argv[3]
    date = sys.argv[4]
    # current_time = time.strftime("%H:%M:%S", time.localtime())
    username = getuser()
    file_path = '/var/spool/samba/'
    full_file_path = file_path + file

    # Get print job name as set from client
    print_job = get_file_name(full_file_path)

    # Get page paper_format
    paper_format = get_file_format(file_path, file)

    # Log incoming job
    format_to_use = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger()
    fh = logging.handlers.RotatingFileHandler('/var/spool/samba/test84.log', maxBytes=10240, backupCount=5)
    fh.setLevel(logging.INFO)  # no matter what level I set here
    formatter = logging.Formatter(format_to_use)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # print("Now it should log something")
    logger.debug(printer + " " + file + " " + print_job + " " + ip + " " + username + " " + date + " " + paper_format)

    q = Queue(connection=Redis())
    # print_job = PrintJob(file, ip, date, printer)
    job = q.enqueue(handle_print_job, args=[ip, printer, date, username, full_file_path, print_job, paper_format])


def get_file_name(file_name):
    print_job_name = ''
    with open(file_name, 'rb') as fh:
        radek = fh.readline().decode('utf-8')
        slova = radek.split()
        while slova[1] != 'ENTER':
            radek = fh.readline().decode('utf-8')
            slova = radek.split()
            if 'JOBNAME' in radek:
                x = re.search("JOBNAME=.*", radek)
                name = x.group(0).split('=')[1]
                print_job_name = name
    return print_job_name


def get_file_format(file_path, file):
    # TODO Check if subprocess run ok
    output_file = file_path + file + ".pdf"
    file_name = file_path + file
    script_path = "/home/filip/Development/ghostpcl-9.50-linux-x86_64/gpcl6-950-linux-x86_64"
    cmd = script_path + " -sDEVICE=pdfwrite -o " + output_file + " " + file_name
    subprocess.getoutput(cmd)
    cmd2 = 'pdfinfo ' + output_file + ' | grep "Page size"'
    out = subprocess.getoutput(cmd2).strip()
    out2 = out.split(":")[1].strip().split(" ")
    a = float(out2[0])
    b = float(out2[2])
    print(a)
    print(b)
    return get_format_from_size(a, b)


def get_format_from_size(a, b):
    # Ensure that a is smaller than b
    if a > b:
        tmp = a
        a = b
        b = tmp
    # TODO add other formats
    if (841 <= a <= 843) and (1189 <= b <= 1191):
        return "A3"
    elif (595 <= a <= 597) and (841 <= b <= 843):
        return "A4"
    elif (419 <= a <= 421) and (594 <= b <= 596):
        return "A5"
    else:
        return "XXX"
