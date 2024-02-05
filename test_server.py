from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models.p2000Message import P2000Message as message
from src.schemas.p2000Message import P2000MessageCreate, P2000Message
import src.dbSeeder

from main import app
from main import get_db

#set database to local database
seedLocal = True
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
    assert response.json() == {'ABP': 'AMBU A2 Ambu 06154 VWS GROENLO Rit 24566 ',
                               'Capcode': '0820154 MKA N-O Gelderland ( Ambulance 06-154 )\n',
                               'Datum': '2022-01-24',
                               'Prioriteit': 1,
                               'Regio': 'Noord en Oost Gelderland',
                               'Tijd': '12:45:09',
                               'id': 12}

def test_non_existing():
    #get non existend message
    response = client.get("/messages/-1")
    assert response.status_code == 404

def test_post_patch_delete():
    #create test message
    message_data = {
         "Datum": "9999-02-16",
         "Tijd": "12:33:12",
         "ABP": "TEST",
         "Prioriteit": 2,
         "Regio": "TEST",
         "Capcode": "999999",
    }

    #post test message
    response = client.post("/messages/", json=message_data)
    assert response.status_code == 201
    
    #get data base and set message id
    db: Session = next(get_db())
    db_message = db.query(message).filter_by(Capcode=message_data["Capcode"]).first()
    message_id = db_message.id
    assert db_message is not None
    
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

#set database to not local database
seedLocal = False