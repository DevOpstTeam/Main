""" Pydantic schemas for the P2000 database. """

from pydantic import BaseModel, ConfigDict
from datetime import date

class P2000MessageBase(BaseModel):
    Datum: date
    Tijd: str
    ABP: str
    Prioriteit: int
    Regio: str
    Capcode: str

class P2000Message(P2000MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class P2000MessageCreate(P2000MessageBase):
    model_config = ConfigDict(from_attributes=True)