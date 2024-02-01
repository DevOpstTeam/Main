from sqlalchemy import Column, Integer, String, Date, Time
from .base import Base

class P2000Message(Base):
    __tablename__ = "site_meldingen"
    id = Column(Integer, primary_key=True, index=True)
    Datum = Column(Date)
    Tijd = Column(String)
    ABP = Column(String)
    Prioriteit = Column(Integer)
    Regio = Column(String)
    Capcode = Column(String)
