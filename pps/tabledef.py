from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from .config import PPS_CONFIG

engine = create_engine('sqlite:///' + PPS_CONFIG.USER_DB, echo=True)
Base = declarative_base()


########################################################################
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password

        # create tables
        Base.metadata.create_all(engine)

# Taken from https://pythonspot.com/login-authentication-with-flask/
########################################################################


class Job(Base):
    __tablename__ = 'jobs'

    time = Column(String)
    printer_name = Column(String)
    job_id = Column(Integer, primary_key=True)
    print_job_name = Column(String)
    page_format = Column(String)
    page_count = Column(String)
    ip = Column(String)
    status = Column(String)

    def __init__(self, job_id, time, printer_name, print_job_name, page_format, page_count, ip, status):
        self.time = time
        self.printer_name = printer_name
        self.job_id = job_id
        self.print_job_name = print_job_name
        self.page_format = page_format
        self.page_count = page_count
        self.ip = ip
        self.status = status

        # create tables
        Base.metadata.create_all(engine)
