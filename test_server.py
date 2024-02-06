from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.p2000Message import P2000Message as message
from src.models.base import Base
from src.schemas.p2000Message import P2000MessageCreate, P2000Message

from main import app, get_db
client = TestClient(app)

def get_test_db():
    from src.models.p2000Message import P2000Message
    """Get a reference to the local test database and close the database when finished."""
    engine = create_engine("sqlite:///test_messages.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if db.query(P2000Message).count == 0:
        messages = [
            P2000Message(id=1,Tijd='12:00:00',Datum='2101-05-10',Regio='Adam',ABP='Politie',Prioriteit=1,Capcode='221231'),
            P2000Message(id=2, Tijd='14:00:00',Datum='2001-07-10',Regio='Rdam',ABP='Ambulance',Prioriteit=1,Capcode='421230'),
            P2000Message(id=3,Tijd='15:00:00',Datum='1101-01-10',Regio='Edam',ABP='Brandweer',Prioriteit=2,Capcode='521237'),
            P2000Message(id=4,Tijd='19:00:00',Datum='2010-06-10',Regio='Zaandam',ABP='Politie',Prioriteit=3,Capcode='921233')
        ]
        db.add_all(messages)
        db.commit()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

#create data for test message
message_data = {
         "id": 5,
         "Tijd": "12:33:12",
         "Datum": "9999-02-16",
         "Regio": "TEST",
         "ABP": "TEST",
         "Prioriteit": 2,
         "Capcode": "999999",
    }
message_id = message_data["id"]

def test_read_main():
    #get default message
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['0 down time cicd werkt!']

def test_read_messages():
    #get all messages
    response = client.get("/messages")
    print(response)
    assert response.status_code == 200

def test_post_message():
    #post test message
    response = client.post("/messages/", json=message_data)
    assert response.status_code == 201

def test_read_posted_message():   
    #get messages just posted
    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200
    
    #check if found message has correct data   
    assert response.json() == {
                            "id": message_id,
                            "Tijd": "12:33:12",
                            "Datum": "9999-02-16",
                            "Regio": "TEST",
                            "ABP": "TEST",
                            "Prioriteit": 2,
                            "Capcode": "999999"}

def test_non_existing():
    #get non existend message
    response = client.get("/messages/-1")
    assert response.status_code == 404

# def test_patch():   
#     #create updated message
#     updated_message_data = {
#         "Tijd": "12:33:12",
#         "Datum": "9999-02-16",
#         "Regio": "TEST",
#         "ABP": "TEST_2",
#         "Prioriteit": 2,
#         "Capcode": "999999"
#     }

#     #modify test message
#     patch_response = client.patch(f"/messages/{message_id}", json=updated_message_data)
#     assert patch_response.status_code == 200
    
#     #update database 
#     db: Session = next(get_test_db())
#     updated_message = db.query(message).filter_by(Capcode=updated_message_data["Capcode"]).first()
#     assert updated_message is not None
#     assert updated_message.ABP == updated_message_data["ABP"]
#     assert updated_message.Capcode == updated_message_data["Capcode"]

def test_delete():
    #delete test message
    del_response = client.delete(f"/messages/{message_id}")
    assert del_response.status_code == 200 
    
    #make sure test message is gone
    response_but_again = client.get(f"/messages/{message_id}") 
    assert response_but_again.status_code == 404

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