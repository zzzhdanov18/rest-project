from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)

session_local = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()
