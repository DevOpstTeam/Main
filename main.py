from fastapi import FastAPI, Depends
from src.schemas.p2000Message import P2000Message as messageSchema
from src.schemas.p2000Message import P2000MessageCreate as messageCreateSchema
from src.models.p2000Message import P2000Message
import src.database as database
# from src.alchemyDatabase import SessionLocal

app = FastAPI()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
def read_root():
    return {"NOVI CICD werkt!"}

# @app.get("/messages")
# def read_messages(db=Depends(get_db)) -> list[messageSchema]:
#     messages = db.query(P2000Message).all()
#     return messages

@app.get("/messages")
def get_messages() -> list[messageSchema]:
    query = "SELECT * FROM site_meldingen;"
    data = database.getData(query)
    
    return data

@app.get("/messages/{message_id}")
def get_message(message_id: int) -> messageSchema:
    query = f'SELECT * FROM site_meldingen WHERE id={message_id}'
    data = database.getData(query)[0]

    return{"id": data["id"], "Datum": data["Datum"], "Tijd": data["Tijd"], "ABP": data["ABP"], "Prioriteit": data["Prioriteit"], "Regio": data["Regio"], "Capcode": data["Capcode"]}

@app.post("/messages/")
def create_message(msg: messageCreateSchema):
    return msg