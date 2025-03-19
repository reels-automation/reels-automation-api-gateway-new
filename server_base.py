import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE URL", DATABASE_URL)
engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)