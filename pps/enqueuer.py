#!/bin/env python3
from redis import Redis
from rq import Queue
from .logic import handle_print_job
from .logger import Logger
from .config import PPS
import sys
from getpass import getuser
import logging
import logging.handlers
import re
import os
import subprocess
import requests
import urllib3.exceptions


def main():
    # TODO check arguments exists
    my_logger = Logger("PPS")
    file = sys.argv[1]
    ip = sys.argv[2]
    printer = sys.argv[3]
    date = sys.argv[4]
    username = getuser()
    file_path = PPS.DIRECTORY_PATH
    full_file_path = file_path + file

    # Get print job name as set from client
    print_job = get_print_job_name(full_file_path, my_logger)

    # Get page paper_format
    paper_format = get_file_format(file_path, file, my_logger)

    # Get page count
    number_of_pages = get_number_of_pages(full_file_path, my_logger)

    # Send to print queue
    job_id = add_to_print_queue(file, file_path, PPS.BLACK_PRINTER, my_logger)

    if job_id is None:
        job_id = "bad_job_id"
    # remove_file("b", my_logger)

    my_logger.warning(printer + " " + file + " " + " " + ip + " " + username + " " + date + " " + print_job + " " +
                      paper_format + " " + number_of_pages + " " + job_id)

    try:
        r = requests.post('http://127.0.0.1:5000', json={
            "jobs": {job_id: {"date": date, 'printer': printer, 'print_job': print_job, 'page_format': paper_format,
                              'number_of_pages': number_of_pages, 'ip': ip, 'status': PPS.PRINT_STATUS["HELD"]}}})
    #     TODO check
    except requests.exceptions.RequestException as e:
        my_logger.critical("Post to Flask server error. Message: " + str(e))


def resume_job(print_job_id, my_logger):
    cmd = "lp -i " + print_job_id + " -H resume"
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0:
        my_logger.critical("Job with id " + print_job_id + " was not sent to printer!!")
        return False
    my_logger.warning("Job with id " + print_job_id + " was sent to printer.")
    return True


def remove_file(full_file_path, my_logger):
    try:
        os.remove(full_file_path)
        my_logger.warning("File " + full_file_path + "deleted")
    except (FileNotFoundError, PermissionError) as e:
        my_logger.critical("File " + full_file_path + "was not deleted")


def add_to_print_queue(file, file_path, printer, my_logger):
    send_to_real_printer(file_path + file, printer, my_logger)
    job_id = get_print_job_id(file, my_logger)
    return job_id


def send_to_real_printer(full_file_name, printer, my_logger):
    cmd = "lpr -P " + printer + " -o job-hold-until=indefinite " + full_file_name
    out = subprocess.getstatusoutput(cmd)
    # TODO Check
    my_logger.warning("Job send to printer" + printer)


def is_printer_online(my_logger):
    try:
        r = requests.get(PPS.BLACK_PRINTER_IP)
        if r.status_code > 300:
            my_logger.critical(PPS.BLACK_PRINTER + " is not online")
            return False
        return True
    except (ConnectionError, OSError) as e:
        my_logger.critical(e)
        return False


def get_print_job_id(file_name, my_logger):
    cmd = "lpq -a | grep " + file_name
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0 or len(out[1].splitlines()) != 1:
        my_logger.critical("Print job id to " + file_name + " not found!")
        return None
    trimmed = " ".join(out[1].split())
    job_id = trimmed.split(" ")[2]
    return job_id


def get_job_id(full_name_path):
    cmd = "sudo /home/printer/bin/job_id.py " + full_name_path
    tmp = os.popen(cmd)
    try:
        job_id = tmp.readlines()[0][:-1]
    except:
        pass

def get_number_of_pages(full_path_name, my_logger):
    cmd = "pkpgcounter"
    out = subprocess.getstatusoutput(cmd + " <" + full_path_name)
    if out[0] != 0:
        my_logger.critical("pkqgcounter error, message: " + out[1])
        return PPS.UNKNOWN_PAGE_COUNT
    return out[1]


def get_print_job_name(full_path_name, my_logger: Logger):
    # ___ will show if no name found
    print_job_name = PPS.UNKNOWN_PRINT_JOB_NAME
    try:
        print_job_name = get_job_name(full_path_name)
    except FileNotFoundError as e:
        my_logger.critical(e)
    return print_job_name


def get_job_name(full_path_name):
    fh = open(full_path_name, 'rb')
    radek = fh.readline().decode('utf-8')
    slova = radek.split()
    while slova[1] != 'ENTER':
        radek = fh.readline().decode('utf-8')
        slova = radek.split()
        if 'JOBNAME' in radek:
            x = re.search("JOBNAME=.*", radek)
            name = x.group(0).split('=')[1]
            return name


def get_file_format(file_path, file, my_logger: Logger):
    output_file = file_path + file + ".pdf"
    file_name = file_path + file
    script_path = PPS.GHOSTPCL_LOCATION
    cmd = script_path + " -sDEVICE=pdfwrite -o " + output_file + " " + file_name
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0:
        my_logger.critical("ghostpcl error with message:" + out[1])
        return PPS.UNKNOWN_PAPER_FORMAT
    cmd2 = 'pdfinfo ' + output_file + ' | grep "Page size"'
    out = subprocess.getstatusoutput(cmd2)
    if out[0] != 0:
        my_logger.critical("pdfinfo error with message: " + out[1])
        return PPS.UNKNOWN_PAPER_FORMAT
    formated_out = out[1].strip().split(":")[1].strip().split(" ")
    a = float(formated_out[0])
    b = float(formated_out[2])
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
        return PPS.UNKNOWN_PAPER_FORMAT


