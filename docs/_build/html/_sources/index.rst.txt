.. PPS_CONFIG documentation master file, created by
   sphinx-quickstart on Thu Feb  6 22:46:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PPS - Python Print Server
=========================

.. toctree::
   :maxdepth: 4

   usage
   config
   source_code
   test



About
=====
PPS - Python Print Server is print server with web interface to show information about print jobs. It counts page format,
number of pages and other information to user.

Instalation
===========
First ensure you habe you need to install python-dev packages


.. code-block::

   git clone git@github.com:philips558/PPS.git
   cd pps
   python3 setup.py install
   cd PPS/pkpgcounter-3.50
   python setup.py install
