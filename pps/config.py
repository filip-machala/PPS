class PPS:
    PAPER_FORMAT = {
        'A4': "A4",
        "A3": "A3",
        "letter": "letter",
        "unknown": "unknown"
    }
    UNKNOWN_PAPER_FORMAT = "unknown"
    DIRECTORY_PATH = '/var/spool/samba/'
    GHOSTPCL_LOCATION = "/home/filip/Development/ghostpcl-9.50-linux-x86_64/gpcl6-950-linux-x86_64"
    LOG_FILE = "PPS_LOG.log"
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    UNKNOWN_PAGE_COUNT = "unknown"
    UNKNOWN_PRINT_JOB_NAME = "unknown Print Job name"

    BLACK_PRINTER = "HP_Print"
    BLACK_PRINTER_IP = "http://192.168.1.49"

    PRINT_STATUS = {
        "HELD": "Held",
        "PRINTING": "Printing",
        "DONE": "Done"
    }
    DRY_RUN = False
