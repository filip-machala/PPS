#!/bin/env python3
from redis import Redis
from rq import Queue
from print_job import PrintJob
from logic import handle_print_job
import sys
from logger import Logger


def main():
    pass
    file = sys.argv[1]
    ip = sys.argv[2]
    path = sys.argv[3]
    date = sys.argv[4]
    q = Queue(connection=Redis())
    print_job = PrintJob(file, ip, date, path)
    job = q.enqueue(handle_print_job, args=[print_job])
    logger = Logger()
    logger.write_to_file(print_job)



if __name__ == '__main__':
    main()