from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.p2000Message import Meldingen as message
from src.schemas.p2000Message import P2000MessageCreate

from main import app, default_message, get_db, update_message

client = TestClient(app)

def get_test_db():
    #Get a reference to the local test database and close the database when finished.
    engine = create_engine("sqlite:///test_messages.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if db.query(message).count == 0:
        messages = [
            message(Tijd='12:00:00',Datum='2101-05-10',regio_id=2,abp_id=3,Prioriteit=1),
            message(Tijd='14:00:00',Datum='2001-07-10',regio_id=18,abp_id=1,Prioriteit=1),
            message(Tijd='15:00:00',Datum='1101-01-10',regio_id=12,abp_id=2,Prioriteit=2),
            message(Tijd='19:00:00',Datum='2010-06-10',regio_id=4,abp_id=3,Prioriteit=3)
        ]
        db.add_all(messages)
        db.commit()
    try:
        yield db
    finally:
        db.close()

#overwrite get_db with get_test_db in app
app.dependency_overrides[get_db] = get_test_db

def test_read_main():
    #get default message
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == default_message

def test_read_messages():
    #get all messages
    response = client.get("/messages")
    assert response.status_code == 200

def test_non_existing():
    #get non existend message
    response = client.get("/messages/-1")
    assert response.status_code == 404

#create data for test message
message_data = {
         "tijd": "11:33:12",
         "datum": "9999-02-16",
         "regio_id": 1,
         "abp_id": 2,
         "prioriteit": 2,
    }

def get_message_id():
    # post test message
    response = client.post("/messages/", json=message_data)
    assert response.status_code == 201
    
    # look for message in database
    db: Session = next(get_test_db())
    message_id = response.json()['melding_id']
    posted_message = db.query(message).filter_by(melding_id=message_id).first()
    db.close()
    
    # if message found return id
    if posted_message:
        return message_id
    else:
        return 0

message_id = get_message_id()

def test_post_message():
    #get message just posted
    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200

    #check if found message has correct data   
    assert response.json() == {
                            "tijd": "11:33:12",
                            "datum": "9999-02-16",
                            "regio_id": 1,
                            "abp_id": 2,
                            "prioriteit": 2,
                            "melding_id": message_id}

def test_update_message():   
    #modify test message
    updated_message_data = P2000MessageCreate(
        tijd="11:33:12",
        datum="1999-02-06",
        regio_id=4,
        abp_id=2,
        prioriteit=2,
    )

    #modify test message
    db: Session = next(get_test_db())
    updated_message = update_message(message_id=message_id, newMessage=updated_message_data, db=db)
    
    #update database 
    db: Session = next(get_test_db())
    updated_message = db.query(message).filter_by(melding_id=message_id).first()
    assert updated_message is not None
    assert updated_message.abp_id == updated_message_data.abp_id
    db.close()

def test_delete():
    #check if message was deleted
    del_response = client.delete(f"/messages/{message_id}")
    assert del_response.status_code == 200 
    
    #make sure test message is gone
    response_deleted = client.get(f"/messages/{message_id}") 
    assert response_deleted.status_code == 404

def test_filter():
    #test case with all parameters
    response = client.get("/messages?dateStart=01-01-2024&dateEnd=01-04-2024&timeStart=12:00&timeEnd=13:00&abp=3&priority=1&region=Groningen")
    assert response.status_code == 200

    #test case with only dateStart parameter
    response = client.get("/messages?dateStart=01-01-2023")
    assert response.status_code == 200

    #test case with dateStart + priority
    response = client.get("/messages?dateStart=02-01-2023&priority=2")
    assert response.status_code == 200

    #test case with invalid priority
    response = client.get("/messages?priority=b")
    assert response.status_code == 422

def test_safest():
    #test case to test safest region method
    response = client.get("/safest")
    assert response.status_code == 200

    #test with start date filter
    response = client.get("/safest?dateStart=06-03-2024")
    assert response.status_code == 200

    #test with inversed filter
    response = client.get("/safest?inversed=True")
    assert response.status_code == 200