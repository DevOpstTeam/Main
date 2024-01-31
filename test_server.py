import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging 
import pytest
import pymysql

from src.models.base import Base
from test_database import init_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector:///{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_HOST")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}'
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
    response = client.get('/message/')
    assert response.status_code == 200
