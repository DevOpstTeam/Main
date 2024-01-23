from pydantic import BaseModel, ConfigDict
from datetime import datetime

class P2000MessageBase(BaseModel):
    Datum: datetime
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