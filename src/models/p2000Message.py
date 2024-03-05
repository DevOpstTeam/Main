""" Pydantic models for the P2000 database. """

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

#Regio model
class Regio(Base):
    __tablename__ = 'regio'
    regio_id = Column(Integer, primary_key=True, autoincrement=True)
    regio_naam = Column(String(255), nullable=False)

#ABP model
class ABP(Base):
    __tablename__ = 'abp'
    abp_id = Column(Integer, primary_key=True, autoincrement=True)
    abp_naam = Column(String(255), nullable=False)

#Meldingen model
class Meldingen(Base):
    __tablename__ = 'meldingen'
    melding_id = Column(Integer, primary_key=True, autoincrement=True)
    regio_id = Column(Integer, ForeignKey('regio.regio_id'))
    abp_id = Column(Integer, ForeignKey('abp.abp_id'))
    prioriteit = Column(Integer)
    datum = Column(String(255))
    tijd = Column(String(255))
    #Relaties opzetten
    regio = relationship("Regio")
    abp = relationship("ABP")
