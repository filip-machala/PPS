# PPS - Python Print Server

This project contains application with working name Python Print Server. It should provide automation in process in real copy center. 
It should should create "proxy" between clients computers and printers to provide information about actual print queue to employees. 

## Assignment
Create print server written in python with following properties.
* It can communicate with multiple printers.
* It can communicate with multiple clients.
* All clients must authorize to use it.
* It has GUI that shows real time information about printing queue to employees. It shows task details: printer, client, format, number of pages and if it is colour or grayscale print.
* It has acceptance mode when client sends anything to printer, task is stopped and needs to be accepted by employee and then it is proceeded to printer.
* It logs all data, to enable reporting in future.
