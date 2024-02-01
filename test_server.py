from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['cicd werkt!!']

def test_read_messages():
    response = client.get("/messages")
    assert response.status_code == 200

def test_read_message_12():
    response = client.get("/messages/12")
    assert response.status_code == 200
    assert response.json() == {'ABP': 'AMBU A2 Ambu 06154 VWS GROENLO Rit 24566 ',
                               'Capcode': '0820154 MKA N-O Gelderland ( Ambulance 06-154 )\n',
                               'Datum': '2022-01-24T00:00:00',
                               'Prioriteit': 1,
                               'Regio': 'Noord en Oost Gelderland',
                               'Tijd': '12:45:09',
                               'id': 12}

def test_non_existing():
    response = client.get("/messages/-1")
    assert response.status_code == 404

# def test_ceate():
#     return