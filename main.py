from fastapi import FastAPI, HTTPException, Depends
from src.schemas.p2000Message import P2000Message as messageSchema
from src.schemas.p2000Message import P2000MessageCreate as messageCreateSchema
from src.models.p2000Message import P2000Message
from src.alchemyDatabase import SessionLocal
from datetime import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"0 down time cicd werkt!"}

@app.get("/messages")
def read_messages(db=Depends(get_db)) -> list[messageSchema]:
    messages = db.query(P2000Message).all()
    return messages

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

@app.get("/messages/{message_id}")
def read_message(message_id: int, db=Depends(get_db)) -> messageSchema:
    message = db.query(P2000Message).filter(P2000Message.id == message_id).first()
    if message == None:
        raise HTTPException(status_code=404, detail=f'message with ID {message_id} not found')
    return message

@app.delete("/messages/{message_id}", status_code=200)
def delete_message(message_id: int, db = Depends(get_db)):
    message = db.query(P2000Message).filter(P2000Message.id == message_id).first()
    db.delete(message)
    db.commit()

@app.patch("/message/{message_id}")
def update_message(newMessage: messageSchema, db = Depends(get_db)):
    message = db.query(P2000Message).filter(P2000Message.id == newMessage.id).first()
    message.update({P2000Message.Datum: newMessage.Datum,
                    P2000Message.Tijd: newMessage.Tijd,
                    P2000Message.ABP: newMessage.ABP,
                    P2000Message.Prioriteit: newMessage.Prioriteit,
                    P2000Message.Regio: newMessage.Regio,
                    P2000Message.Capcode: newMessage.Capcode})
    db.commit()

@app.get("/messages/filter/")
def filter_messages(dateStart: str | None = None, dateEnd: str | None = None, timeEnd: str | None = None, 
                    timeStart: str | None = None, abp: str | None = None, priority:int | None = None, 
                    region: str | None = None, capcode: str | None = None, db=Depends(get_db)) -> list[messageSchema]:
    messages = db.query(P2000Message)
    if dateStart != None:
        dateFormat = "%d-%M-%Y"
        startDate = datetime.strptime(dateStart, dateFormat)
        messages = messages.filter(P2000Message.Datum >= startDate)

        if dateEnd != None:
            endDate = datetime.strptime(dateEnd, dateFormat)
            messages = messages.filter(P2000Message.Datum <= endDate)
    if timeStart != None:
        messages = messages.filter(P2000Message.Tijd > timeStart)
    if timeEnd != None:
        messages = messages.filter(P2000Message.Tijd < timeEnd)
    if abp != None:
        messages = messages.filter(P2000Message.ABP.contains(abp))
    if priority != None:
        messages = messages.filter(P2000Message.Prioriteit == priority)
    if region != None:
        messages = messages.filter(P2000Message.Regio == region)
    if capcode != None:
        messages = messages.filter(P2000Message.Capcode.contains(capcode))
    return messages.all()