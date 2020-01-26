#!/bin/env python3
import time


def main():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file = open("/var/spool/samba/log.txt", "w")
    file.write(current_time)
    file.close()


if __name__ == '__main__':
    main()