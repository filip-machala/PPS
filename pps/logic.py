#!/bin/env python3
from .logger import Logger
from .config import PPS_CONFIG
import sys
from getpass import getuser
import re
import os
import subprocess
import requests


def main():
    # TODO check arguments exists
    my_logger = Logger("PPS_CONFIG")
    file = sys.argv[1]
    ip = sys.argv[2]
    printer = sys.argv[3]
    date = sys.argv[4]
    username = getuser()
    file_path = PPS_CONFIG.DIRECTORY_PATH
    full_file_path = file_path + file
    handle_enqueue(my_logger, file, ip, printer, date, username, file_path, full_file_path)


def handle_enqueue(my_logger: Logger, file: str, ip: str, printer: str, date: str, username: str, directory_path: str,
                   full_file_path: str):
    """
    Handle enqueue process. Get all info about print job and add it to queue. Then send info to server for acknowledgement.
    :param my_logger: Logger class for logging.
    :param file: str file name
    :param ip: str ip address of client that has sent print job
    :param printer: str name of virtual printer that received print job
    :param date: str datetime of print job
    :param username: str name of user that has sent print job
    :param directory_path: str path to directory of file.
    :param full_file_path: str absolute path to file that should be sent to printer
    :return:
    """
    # Get print job name as set from client
    print_job = get_print_job_name(full_file_path, my_logger)

    # Get page paper_format
    paper_format = get_file_format(directory_path, file, my_logger)

    # Get page count
    number_of_pages = get_number_of_pages(full_file_path, my_logger)

    # Send to print queue
    job_id = add_to_print_queue(file, directory_path, PPS_CONFIG.BLACK_PRINTER, my_logger)

    my_logger.warning(printer + " " + file + " " + " " + ip + " " + username + " " + date + " " + print_job + " " +
                      paper_format + " " + number_of_pages + " " + job_id)

    try:
        r = requests.post('http://127.0.0.1:5000', json={
            "jobs": {job_id: {"date": date, 'printer': printer, 'print_job': print_job, 'page_format': paper_format,
                              'number_of_pages': number_of_pages, 'ip': ip,
                              'status': PPS_CONFIG.PRINT_STATUS["HELD"]}}})
    #     TODO check
    except requests.exceptions.RequestException as e:
        my_logger.critical("Post to Flask server error. Message: " + str(e))


def resume_job(print_job_id: str, my_logger: Logger) -> bool:
    """
    Resume job that is in print queue. This function uses lp command.
    :param print_job_id: str id of print job to resume
    :param my_logger: Logger class for logging.
    :return: True if lp command return 0.
    """
    cmd = "lp -i " + print_job_id + " -H resume"
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0:
        my_logger.critical("Job with id " + print_job_id + " was not sent to printer!!")
        return False
    my_logger.warning("Job with id " + print_job_id + " was sent to printer.")
    return True


def remove_file(full_file_path: str, my_logger: Logger):
    """
    Delete file from disk.
    :param full_file_path: str absolute path to file that should be sent to printer
    :param my_logger: Logger class for logging.
    :return: nothing
    """
    try:
        os.remove(full_file_path)
        my_logger.warning("File " + full_file_path + "deleted")
    except (FileNotFoundError, PermissionError) as e:
        my_logger.critical("File " + full_file_path + "was not deleted")


def add_to_print_queue(file: str, directory_path: str, printer: str, my_logger: Logger) -> str:
    """
    Add job to print queue and return print job id. If any error occurs return value of UNKNOWN_PRINT_JOB_ID in config.
    :param file: str file name
    :param directory_path: str path to directory of file.
    :param printer: str name of installed printer in CUPS server.
    :param my_logger: Logger class for logging.
    :return: str job id or UNKNOWN_PRINT_JOB_ID in config.
    """
    send_to_real_printer(directory_path + file, printer, my_logger)
    job_id = get_print_job_id(file, my_logger)
    return job_id


def send_to_real_printer(full_file_name: str, printer: str, my_logger: Logger):
    """
    Send job to real printer given as argument. This function uses lpr to send job to printer.
    :param full_file_name: str absolute path to file that should be sent to printer
    :param printer: str name of installed printer in CUPS server.
    :param my_logger: Logger class for logging.
    :return: nothing
    """
    cmd = "lpr -P " + printer + " -o job-hold-until=indefinite " + full_file_name
    out = subprocess.getstatusoutput(cmd)
    # TODO Check
    my_logger.warning("Job send to printer" + printer)


def is_printer_online(my_logger: Logger) -> bool:
    """
    Check if printer is online. This function simple load printer administration page.
    :param my_logger: Logger class for logging.
    :return: bool True if print is online.
    """
    try:
        r = requests.get(PPS_CONFIG.BLACK_PRINTER_IP)
        if r.status_code > 300:
            my_logger.critical(PPS_CONFIG.BLACK_PRINTER + " is not online")
            return False
        return True
    except (ConnectionError, OSError) as e:
        my_logger.critical(e)
        return False


def get_print_job_id(file_name: str, my_logger: Logger) -> str:
    """
    Get print job id from print queue. This function uses bash lpq.
    :param file_name: str name of file to search for in print queue.
    :param my_logger: Logger class for logging.
    :return: str print job id or value of UNKNOWN_PRINT_JOB_ID from config.
    """
    cmd = "lpq -a | grep " + file_name
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0 or len(out[1].splitlines()) != 1:
        my_logger.critical("Print job id to " + file_name + " not found!")
        return PPS_CONFIG.UNKNOWN_PRINT_JOB_ID
    trimmed = " ".join(out[1].split())
    job_id = trimmed.split(" ")[2]
    return job_id


def get_number_of_pages(full_path_name: str, my_logger: Logger) -> str:
    """
    Get number of pages. This function uses pkpgcounter bash command to count pages.
    :param full_path_name: str absolute path to file.
    :param my_logger: Logger class for logging.
    :return: str number of pages or value of UNKNOWN_PAGE_COUNT from config.
    """
    cmd = "pkpgcounter"
    out = subprocess.getstatusoutput(cmd + " <" + full_path_name)
    if out[0] != 0:
        my_logger.critical("pkqgcounter error, message: " + out[1])
        return PPS_CONFIG.UNKNOWN_PAGE_COUNT
    return out[1]


def get_print_job_name(full_path_name: str, my_logger: Logger) -> str:
    """
    Get print job name from file in PCL6 format.
    :param full_path_name: str absolute path to file.
    :param my_logger: Logger class for logging.
    :return: str print job name or value of UNKNOWN_PRINT_JOB_NAME from config.
    """
    try:
        fh = open(full_path_name, 'rb')
        radek = fh.readline().decode('utf-8')
        slova = radek.split()
        while slova[1] != 'ENTER':
            radek = fh.readline().decode('utf-8')
            slova = radek.split()
            if 'JOBNAME' in radek:
                x = re.search("JOBNAME=.*", radek)
                name = x.group(0).split('=')[1]
                return name[1:-1]
    except (IndexError, FileNotFoundError) as e:
        my_logger.critical(e)
        return PPS_CONFIG.UNKNOWN_PRINT_JOB_NAME


def get_file_format(directory_path: str, file: str, my_logger: Logger) -> str:
    """ 
    Get file format from print file. Firstly create temporary pdf document with ghostpcl, then use pdfinfo and get 
    page count. 
    :param directory_path: str path to directory of file.
    :param file: str file name.
    :param my_logger: Logger class for logging.
    :return: str paper format or value of UNKNOWN_PAPER_FORMAT from config if any error occurs. 
    """""
    output_file = directory_path + file + ".pdf"
    file_name = directory_path + file
    script_path = PPS_CONFIG.GHOSTPCL_LOCATION
    cmd = script_path + " -sDEVICE=pdfwrite -o " + output_file + " " + file_name
    out = subprocess.getstatusoutput(cmd)
    if out[0] != 0:
        my_logger.critical("ghostpcl error with message:" + out[1])
        return PPS_CONFIG.UNKNOWN_PAPER_FORMAT
    cmd2 = 'pdfinfo ' + output_file + ' | grep "Page size"'
    out = subprocess.getstatusoutput(cmd2)
    if out[0] != 0:
        my_logger.critical("pdfinfo error with message: " + out[1])
        remove_file(output_file, my_logger)
        return PPS_CONFIG.UNKNOWN_PAPER_FORMAT
    remove_file(output_file, my_logger)
    formated_out = out[1].strip().split(":")[1].strip().split(" ")
    a = float(formated_out[0])
    b = float(formated_out[2])
    return get_format_from_size(a, b)


def get_format_from_size(a: float, b: float) -> str:
    """
    Return file format from size in pixels. Return unknown paper format if nothing is matched.
    :param a: float smaller size of document
    :param b: float bigger size of document
    :return: str file format
    """
    # Ensure that a is smaller than b if other orientation is selected
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
        return PPS_CONFIG.UNKNOWN_PAPER_FORMAT


