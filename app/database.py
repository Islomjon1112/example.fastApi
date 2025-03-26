from sqlmodel import SQLModel, Field, create_engine, Column, TIMESTAMP, text
from sqlalchemy.orm import Session
import psycopg
import time
from .config import settings

# Database URL (Make sure it's set properly for PostgreSQL)
DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session

# while True:
#     try:
#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastApi",
#             user="postgres",
#             password="malika1802"
#         )
#         cursor = conn.cursor()
#         print("Database connection was succesfull ")
#         break

#     except psycopg.OperationalError as error:
#         print("connection to database was failed")
#         print("Error: ", error)
#         time.sleep(2)