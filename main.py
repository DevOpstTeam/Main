from fastapi import FastAPI, HTTPException, Depends
from src.schemas.p2000Message import P2000Message as messageSchema
from src.schemas.p2000Message import P2000MessageCreate as messageCreateSchema
from src.models.p2000Message import P2000Message
from src.alchemyDatabase import SessionLocal

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