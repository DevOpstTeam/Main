""" SQLAlchemy database

Create a connection to the P2000 database using SQLAlchemy.
Import SessionLocal from this script to make use of the database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = 'oop'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)