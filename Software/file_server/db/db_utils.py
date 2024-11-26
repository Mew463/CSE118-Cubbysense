from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os
from consts import DATABASE_URL
from db.models import LED

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables if they don't exist
def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

# Dependency that provides a new session for each request
def get_session():
    with Session(engine) as session:
        yield session

# Initially seed the 4 leds into the table
def seed_leds():
    with Session(engine) as session:
        # Insert the 4 leds
        session.add(LED(color="red"))
        session.add(LED(color="green"))
        session.add(LED(color="blue"))
        session.add(LED(color="yellow"))
        session.commit()