""" Pydantic schemas for the P2000 database. """

from pydantic import BaseModel
from datetime import date
from typing import Optional


#regio 
class Regio(BaseModel):
    regio_id: int
    regio_naam: str

#abp 
class ABP(BaseModel):
    abp_id: int
    abp_naam: str

#melding
class P2000MessageBase(BaseModel):
    datum: date  
    tijd: str   
    prioriteit: int 
    regio: Optional[Regio] = None
    abp: Optional[ABP] = None

# create message
class P2000MessageCreate(P2000MessageBase):
    abp_id: int
    regio_id: int

# read message
class P2000Message(P2000MessageBase):
    melding_id: int
