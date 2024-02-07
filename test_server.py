from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.p2000Message import P2000Message as message
from src.schemas.p2000Message import P2000MessageCreate

from main import app, get_db, update_message

client = TestClient(app)

def get_test_db():
    #Get a reference to the local test database and close the database when finished.
    engine = create_engine("sqlite:///test_messages.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if db.query(message).count == 0:
        messages = [
            message(id=1,Tijd='12:00:00',Datum='2101-05-10',Regio='Adam',ABP='Politie',Prioriteit=1,Capcode='221231'),
            message(id=2, Tijd='14:00:00',Datum='2001-07-10',Regio='Rdam',ABP='Ambulance',Prioriteit=1,Capcode='421230'),
            message(id=3,Tijd='15:00:00',Datum='1101-01-10',Regio='Edam',ABP='Brandweer',Prioriteit=2,Capcode='521237'),
            message(id=4,Tijd='19:00:00',Datum='2010-06-10',Regio='Zaandam',ABP='Politie',Prioriteit=3,Capcode='921233')
        ]
        db.add_all(messages)
        db.commit()
    try:
        yield db
    finally:
        db.close()

#overwrite get_db with get_test_db in app
app.dependency_overrides[get_db] = get_test_db

#create data for test message
message_data = {
         "Tijd": "11:33:12",
         "Datum": "9999-02-16",
         "Regio": "TEST",
         "ABP": "TEST",
         "Prioriteit": 2,
         "Capcode": "9998999"
    }

def test_read_main():
    #get default message
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['0 down time cicd werkt!']

def test_read_messages():
    #get all messages
    response = client.get("/messages")
    assert response.status_code == 200

def test_non_existing():
    #get non existend message
    response = client.get("/messages/-1")
    assert response.status_code == 404

def test_post_message():
    #post test message
    response = client.post("/messages/", json=message_data)
    assert response.status_code == 201
    
    #check in database
    db: Session = next(get_test_db())
    posted_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    assert posted_message is not None
    db.close()

def test_read_posted_message():   
    #find posted message in database
    db: Session = next(get_test_db())
    posted_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    assert posted_message is not None
    message_id = posted_message.id

    #get message just posted
    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200

    #check if found message has correct data   
    assert response.json() == {
                            "Tijd": "11:33:12",
                            "Datum": "9999-02-16",
                            "Regio": "TEST",
                            "ABP": "TEST",
                            "Prioriteit": 2,
                            "Capcode": "9998999",
                            "id": message_id}
    db.close()

#modify test message
def test_update_message():   
    #find posted message in database
    db: Session = next(get_test_db())
    posted_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    assert posted_message is not None

    #create updated message
    message_id = posted_message.id
    updated_message_data = P2000MessageCreate(
        Tijd="11:33:12",
        Datum="1999-02-06",
        Regio="TEST",
        ABP="TEST_2",
        Prioriteit=2,
        Capcode="9998999"
    )

    #modify test message
    updated_message =update_message(message_id=message_id, newMessage=updated_message_data, db=db)
    
    #update database 
    db: Session = next(get_test_db())
    updated_message = db.query(message).filter_by(Capcode=updated_message_data.Capcode).first()
    assert updated_message is not None
    assert updated_message.ABP == updated_message_data.ABP
    assert updated_message.Capcode == updated_message_data.Capcode

def test_delete():
    #find posted message in database
    db: Session = next(get_test_db())
    posted_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    assert posted_message is not None
    message_id = posted_message.id
    
    #check if message was deleted
    del_response = client.delete(f"/messages/{message_id}")
    assert del_response.status_code == 200 
    
    #make sure test message is gone
    response_deleted = client.get(f"/messages/{message_id}") 
    assert response_deleted.status_code == 404
    db.close()

def test_filter():
    #test case with all parameters
    response = client.get("/messages/filter/?dateStart=01-01-2023&dateEnd=01-02-2023&timeStart=12:00&timeEnd=13:00&abp=test&priority=1&region=test&capcode=123")
    assert response.status_code == 200

    #test case with only dateStart parameter
    response = client.get("/messages/filter/?dateStart=01-01-2023")
    assert response.status_code == 200

    #test case with dateStart + priority
    response = client.get("/messages/filter/?dateStart=02-01-2023&priority=2")
    assert response.status_code == 200

    #test case with invalid priority
    response = client.get("/messages/filter/?priority=b")
    assert response.status_code == 422