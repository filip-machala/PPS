Usage
=====

After installing Python Print Server you need to setup following:

1. Configure printer in CUPS server and enter it's name in config. There are currently available two printers to set.

.. code-block::

    BLACK_PRINTER
    COLOR_PRINTER

2. Setup samba to share virtual network printer that will run queueing new jobs.
Be sure this following options are set in samba config.

.. code-block::

    [global]
    rpc_server:spoolss = external
    rpc_daemon:spoolssd = fork
    load printers = no
    printing = bsd

    [filip_printer]
      path = /var/spool/samba
      print command = python3 -m pps "%s" "%I" "%p" "%T"
      comment = HP Shared printer
      printable = yes
      browsable = yes
      writable = no
      guest ok = yes

After this there should be network share //server_ip/filip_printer.

3. You need to create database with users for authentication. For this purpose you can use dummy.py script as example.
Program expects users database with name "pps.db".

4. Control settings in config. More about in :ref:`config`.

5. Then you can start Flask server.

.. code-block::

    export FLASK_APP=server.py
    flask run

6. Now you can access web interface http://127.0.0.1:5000/. You need to authenticate with user credentials in db.