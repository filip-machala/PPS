Need to install  
sudo apt-get install libcups2-dev
sudo apt install python3-dev
sudo apt-get install cups samba
pip3 install rq
sudo apt install redis-server



In smb.conf set in [global] 
rpc_server:spoolss = external
rpc_daemon:spoolssd = fork
load printers = no
printing = bsd

and add section
[filip_printer]
  path = /var/spool/samba
  print command = /usr/bin/python3 /home/filip/Development/PPS/CUPS/monitor.py "%s" "%I" "%p" "%T"
  comment = HP Shared printer
  printable = yes
  browsable = yes
  writable = no
  guest ok = yes

and comment [printers] section

https://help.ubuntu.com/lts/serverguide/cups.html
Not necessary
Install pycups
pip3 install pycups
