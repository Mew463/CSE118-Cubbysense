from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os
from consts import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables if they don't exist
def create_db_and_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

# Dependency that provides a new session for each request
def get_session():
    with Session(engine) as session:
        yield session
