# Example of how to add users to database

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///users.db', echo=True)
engine.connect()
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin","admin")
session.add(user)

user = User("python","python")
session.add(user)

user = User("jumpiness","python")
session.add(user)

# commit the record the database
session.commit()

session.commit()
