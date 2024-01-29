import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.base import Base

SQLALCHEMY_DATABASE_URL = "mysql:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from models.p2000Message import P2000Message

    Base.metadata.create_all(bind=engine)
    seed_db()

def seed_db(): 
    print('Seeding DB')

    from models.p2000Message import P2000Message as message

    db = SessionLocal

    if db.query(message).count == 0:
        messages = [
            message(Tijd='12:00:00',Datum='2101-05-10',Regio='Adam',ABP='Politie',Prioriteit=1,Capcode='221231'),
            message(Tijd='14:00:00',Datum='2001-07-10',Regio='Rdam',ABP='Ambulance',Prioriteit=1,Capcode='421230'),
            message(Tijd='15:00:00',Datum='1101-01-10',Regio='Edam',ABP='Brandweer',Prioriteit=2,Capcode='521237'),
            message(Tijd='19:00:00',Datum='2010-06-10',Regio='Zaandam',ABP='Politie',Prioriteit=3,Capcode='921233')
        ]
        db.add_all(messages)
        db.commit()
    db.close()