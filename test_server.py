import os

from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging 
import pytest

from main import app
from test_database import init_db
from models.base import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL

# db_url = URL.create(
#     "mysql",
#     username=os.environ.get("MYSQL_USER"),
#     password=os.environ.get("MYSQL_PASSWORD"),
#     host=os.environ.get("MYSQL_HOST"),
#     port=os.environ.get("MYSQL_PORT"),
#     database=os.environ.get("MYSQL_DB")
# )

SQLALCHEMY_DATABASE_URL = f'mysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_HOST")}:{os.environ.get("MYSQL_PORT", 25060)}/{os.environ.get("MYSQL_DB")}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
