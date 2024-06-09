from sqlalchemy import Column, Integer, ARRAY, String, Boolean, DateTime, Date, Table
from db.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column((String(32)), nullable=True)
    unique_id = Column((String(32)),unique=True, nullable=False)
    generated_code = Column(String(32), nullable=True)
    add_code = Column(String(32), nullable=True)
    coin = Column(String(32), nullable=False , default="500")
    