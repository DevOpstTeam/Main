from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from main import get_db

engine = create_engine("sqlite:///test_messages.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#set database to local database
app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

def test_read_main():
    #get default message
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['0 down time cicd werkt!']

def test_read_messages():
    #get all messages
    response = client.get("/messages")
    assert response.status_code == 200

def test_read_message_12():
    #get message with id 12
    response = client.get("/messages/12")
    assert response.status_code == 200
    
    #check if found message has correct data   
    assert response.json() == {'ABP': 'AMBU',
                               'Capcode': '0820157',
                               'Datum': '2024-02-06',
                               'Prioriteit': 2,
                               'Regio': 'Noord en Oost Gelderland',
                               'Tijd': '11:03:03',
                               'id': 12}

def test_non_existing():
    #get non existend message
    response = client.get("/messages/-1")
    assert response.status_code == 404

def test_post_patch_delete():
    #post test message
    response = client.post("/messages/", json={
        'Datum':"9999-02-16",
        'Tijd':"12:00:00",
        'ABP':"TEST",
        'Prioriteit':2,
        'Regio':"TEST_REGIO",
        'Capcode':"999999" 
    })
    assert response.status_code == 201
    
    # get the message ID from the post response
    db_message = response.json()
    assert db_message is not None
    test_message_id = db_message["id"]
    
    # #create updated message
    # updated_message_data = {
    #     "Datum": "9999-02-16",
    #     "Tijd": "12:33:12",
    #     "ABP": "TEST_2",
    #     "Prioriteit": 2,
    #     "Regio": "TEST",
    #     "Capcode": "999999"
    # }

    # #modify test message
    # patch_response = client.patch(f"/messages/{message_id}", json=updated_message_data)
    # assert patch_response.status_code == 200
    
    # #update database 
    # db: Session = next(get_db())
    # updated_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    # assert updated_message is not None
    # assert updated_message.ABP == updated_message_data["ABP"]
    # assert updated_message.Capcode == updated_message_data["Capcode"]

    #delete test message
    del_response = client.delete(f"/messages/{test_message_id}")
    assert del_response.status_code == 200 
    
    #make sure test message is gone
    response_but_again = client.get(f"/messages/{test_message_id}") 
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