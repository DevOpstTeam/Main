from sqlalchemy import Column, Integer, String, DateTime
from .base import Base
import os

class P2000Message(Base):
    __tablename__ = "site_meldingen"
    id = Column(Integer, primary_key=True, index=True)
    Datum = Column(DateTime)
    Tijd = Column(String)
    ABP = Column(String)
    Prioriteit = Column(Integer)
    Regio = Column(String)
    # TODO Use relationship for many to many relations
    Capcode = Column(String)
