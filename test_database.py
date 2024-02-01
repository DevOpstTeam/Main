# import os

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import pymysql
# from src.models.base import Base

# SQLALCHEMY_DATABASE_URL = f'mysql:///{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_HOST")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def init_db():
#     from src.models.p2000Message import P2000Message

#     Base.metadata.create_all(bind=engine)
#     seed_db()


# def seed_db(): 
#     print('Seeding DB')

#     from src.models.p2000Message import P2000Message
#     db = SessionLocal()

#     if db.query(P2000Message).count == 0:
#         messages = [
#             P2000Message(Tijd='12:00:00',Datum='2101-05-10',Regio='Adam',ABP='Politie',Prioriteit=1,Capcode='221231'),
#             P2000Message(Tijd='14:00:00',Datum='2001-07-10',Regio='Rdam',ABP='Ambulance',Prioriteit=1,Capcode='421230'),
#             P2000Message(Tijd='15:00:00',Datum='1101-01-10',Regio='Edam',ABP='Brandweer',Prioriteit=2,Capcode='521237'),
#             P2000Message(Tijd='19:00:00',Datum='2010-06-10',Regio='Zaandam',ABP='Politie',Prioriteit=3,Capcode='921233')
#         ]
#         db.add_all(messages)
#         db.commit()
#     db.close()