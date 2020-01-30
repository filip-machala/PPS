#!/bin/env python3
import time
import sys
import subprocess
import os
from subprocess import PIPE, Popen
import getpass
# from pkpgpdls import analyzer

def main():
    FILE = sys.argv[1]
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    username = getpass.getuser()
    file_to_read = "/var/spool/samba/" + FILE
    print(file_to_read)
    # p = analyzer.main(file_to_read)
    cmd = "python /home/filip/Development/pkpgcounter-3.50/pkpgpdls/analyzer.py /var/spool/samba/smbprn.uH3cxO"
    p = subprocess.Popen(cmd)
    # p = subprocess.getstatusoutput("pkpgcounter /var/spool/samba/smbprn.uH3cxO")
    print(p)
    # tmp = p.stdout
    # stderr = p.stderr
    file = open("/var/spool/samba/log.txt", "w")
    # file.write(tmp)
    # file.write(stderr)

    file.write(username)
    file.write(current_time)
    for arg in FILE:
        file.write('\n')
        file.write(arg)
    file.close()
    # print_file = sys.argv[1]
    # file_to_print = "/var/spool/samba/" + print_file
    # print(file_to_print)
    # subprocess.run(["lpr", "-P HP_LaserJet_P2055dn", file_to_print])

    # Send to printer
    # os.system("lpr -P HP_LaserJet_P2055dn " + file_to_print)


if __name__ == '__main__':
    main()