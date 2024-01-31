from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f'mysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_HOST")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)