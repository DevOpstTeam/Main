""" Pydantic schemas for the P2000 database. """

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


#regio 
class Regio(BaseModel):
    regio_id: Optional[int] = None
    regio_naam: str

#abp 
class ABP(BaseModel):
    abp_id: Optional[int] = None
    abp_naam: str

#melding
class P2000MessageBase(BaseModel):
    datum: date  
    tijd: str   
    prioriteit: Optional[int] = None
    regio_id: Optional[int] = None  
    abp_id: Optional[int] = None    

# create message
class P2000MessageCreate(P2000MessageBase):
    pass

# read message
class P2000Message(P2000MessageBase):
    melding_id: int
