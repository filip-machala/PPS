from tabledef import *
from sqlalchemy.orm import sessionmaker


def main():
    print("pok")
    engine = create_engine('sqlite:///pps.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    POST_USERNAME = "admin"
    POST_PASSWORD = "admin"
    result = s.query(User).filter_by(username=POST_USERNAME, password=POST_PASSWORD).first()
    if result:
        print("Good job")

if __name__== "__main__":
  main()