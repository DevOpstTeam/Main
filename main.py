from fastapi import FastAPI, HTTPException, Depends
from src.schemas.p2000Message import P2000Message as messageSchema
from src.schemas.p2000Message import P2000MessageCreate as messageCreateSchema
from src.models.p2000Message import P2000Message
from src.alchemyDatabase import SessionLocal
from datetime import datetime

# class messageFilterType(str, Enum):
#     date = "datum"
#     time = "tijd"
#     abp = "abp"
#     priority = "prioriteit"
#     #region = "regio"
#     capCode = "capcode"

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"NOVI CICD werkt!!!!!"}

@app.get("/messages")
def read_messages(db=Depends(get_db)) -> list[messageSchema]:
    messages = db.query(P2000Message).all()
    return messages

@app.get("/messages/{message_id}")
def read_message(message_id: int, db=Depends(get_db)) -> messageSchema:
    message = db.query(P2000Message).filter(P2000Message.id == message_id).first()
    if message == None:
        raise HTTPException(status_code=404, detail=f'message with ID {message_id} not found')
    return message

@app.post("/messages/", status_code=201)
def create_message(message: messageCreateSchema, db=Depends(get_db)) -> messageSchema:
    db_message = P2000Message(Datum=message.Datum,
                              Tijd=message.Tijd,
                              ABP=message.ABP,
                              Prioriteit=message.Prioriteit,
                              Regio=message.Regio,
                              Capcode=message.Capcode)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/filter/")
def filter_messages(date: str | None = None, timeEnd: str | None = None, timeStart: str | None = None, abp: str | None = None, priority:int | None = None, region: str | None = None, capcode: str | None = None, db=Depends(get_db)):
    messages = db.query(P2000Message)
    if date != None:
        # TODO Fix
        messages = messages.filter(P2000Message.Datum == date)
    if timeStart != None:
        timeFormat = "%H:%M:%S"
        start = datetime.strptime(timeStart, timeFormat)
        if timeEnd != None:
            end = datetime.strptime(timeEnd, timeFormat)
            # TODO Fix
            messages = messages.filter(datetime.strptime(str(f'{P2000Message.Tijd}'), timeFormat) > start and
                                       datetime.strptime(str(f'{P2000Message.Tijd}'), timeFormat) < end)
        else:
            # TODO Fix
            messages = messages.filter(P2000Message.Tijd > start)
    if abp != None:
        messages = messages.filter(P2000Message.ABP == abp)
    if priority != None:
        messages = messages.filter(P2000Message.Prioriteit == priority)
    if region != None:
        messages = messages.filter(P2000Message.Regio == region)
    if capcode != None:
        messages = messages.filter(P2000Message.Capcode.contains(capcode))
    return messages.all()