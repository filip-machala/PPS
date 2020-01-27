#!/bin/env python3
import time
import sys
import subprocess
import os

def main():
    FILE = sys.argv
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    import getpass
    username = getpass.getuser()

    file = open("/var/spool/samba/log.txt", "w")
    file.write(username)
    file.write(current_time)
    for arg in FILE:
        file.write('\n')
        file.write(arg)
    file.close()
    print_file = sys.argv[1]
    file_to_print = "/var/spool/samba/" + print_file
    print(file_to_print)
    # subprocess.run(["lpr", "-P HP_LaserJet_P2055dn", file_to_print])

    # Send to printer
    # os.system("lpr -P HP_LaserJet_P2055dn " + file_to_print)


if __name__ == '__main__':
    main()