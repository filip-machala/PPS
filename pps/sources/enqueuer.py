#!/bin/env python3
from redis import Redis
from rq import Queue
from . import Print_job
from . import logic
import sys


def main():
    file = sys.argv[1]
    ip = sys.argv[2]
    path = sys.argv[3]
    date = sys.argv[4]
    q = Queue(connection=Redis())
    print_job = Print_job.PrintJob(file, ip, date, path)
    job = q.enqueue(logic.handle_print_job, args=print_job)


if __name__ == '__main__':
    main()