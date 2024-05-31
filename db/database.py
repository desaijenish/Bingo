import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

DATABASE_URL = os.getenv('DATABASE_URL', settings.SQLALCHEMY_DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DBBaseModel = declarative_base()