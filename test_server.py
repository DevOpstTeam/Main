import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging 
import pytest

from src.models.base import Base
from test_database import init_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

app = FastAPI()
client = TestClient(app)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_main(test_db):
    response = client.get('/messages/')
    assert response.status_code == 200
