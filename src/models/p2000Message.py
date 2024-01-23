from sqlalchemy import Column, Integer, String
from .base import Base
import os

class P2000Message(Base):
    __tablename__ = os.environ.get('MYSQL_DB')
    id = Column(Integer, primary_key=True, index=True)
    Datum = Column(String)
    Tijd = Column(String)
    ABP = Column(String)
    Prioriteit = Column(Integer)
    Regio = Column(String)
    # TODO Use relationship for many to many relations
    Capcode = Column(String)
