from .printJob import PrintJob


def handle_print_job(print_job: PrintJob):
    file = open("/var/spool/samba/handle_job.txt", "w")
    file.write(print_job.file)
    file.write(print_job.ip)
    file.write(print_job.time)
    file.write(print_job.printer)
    file.close()