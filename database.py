from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


engine = create_engine(f'postgresql://{os.getenv("POSTGRES_USER")}:'
                       f'{os.getenv("POSTGRES_PASSWORD")}@db:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}',
                       echo=True
                       )

Base = declarative_base()

session_local = sessionmaker(bind=engine)
