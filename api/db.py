from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@db:5432/journal")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
