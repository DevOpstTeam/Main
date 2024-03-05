""" SQLAlchemy database

Create a connection to the P2000 database using SQLAlchemy.
Import SessionLocal from this script to make use of the database connection.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = 'mysql://doadmin:AVNS_ct22pEFkDHsEcqTjlIM@db-mysql-ams3-58762-do-user-15578681-0.c.db.ondigitalocean.com:25060/p2000_rapportage'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)