from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@postgresserverURL/db"
my_engin = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=my_engin)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### SQL Coding
# while True:
#     try:
#         conn = psycopg2.connect(host='192.168.111.201', database='fastapi', user='postgres', password='changeme', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull !")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(3)        