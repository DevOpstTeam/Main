from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db

def get_test_db():
    """Get a reference to the local test database and close the database when finished."""
    engine = create_engine("sqlite:///test_messages.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['0 down time cicd werkt!']

def test_read_messages():
    response = client.get("/messages")
    assert response.status_code == 200

def test_read_message_12():
    response = client.get("/messages/12")
    assert response.status_code == 200
    assert response.json() == {'ABP': 'AMBU',
                               'Capcode': '1520999',
                               'Datum': '2024-02-01',
                               'Prioriteit': 2,
                               'Regio': 'Haaglanden',
                               'Tijd': '12:35:28',
                               'id': 12}

def test_non_existing():
    response = client.get("/messages/-1")
    assert response.status_code == 404

# def test_ceate():
#     return