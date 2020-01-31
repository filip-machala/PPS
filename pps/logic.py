# from pps import print_job
import subprocess
import requests


def handle_print_job(ip, printer, date, username, full_file_path, print_job, paper_format):
    """Handle print job"""
    # file = open("/var/spool/samba/handle_job.txt", "w")
    # file.write(print_job.file)
    # file.write(print_job.ip)
    # file.write(print_job.time)
    # file.write(print_job.printer)
    # file.close()

    cmd = "pkpgcounter"
    number_of_pages = subprocess.getoutput(cmd + " <" + full_file_path)
    r = requests.post('http://127.0.0.1:5000', json={"jobs": {print_job: date + " " + printer + " " + username + " " + print_job + " " + paper_format + " " + number_of_pages + " " + ip}})
