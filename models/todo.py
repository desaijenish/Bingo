from sqlalchemy import Column, Integer, ARRAY, String, Boolean, DateTime, Date, Table
from db.base_class import Base
from sqlalchemy.orm import relationship


class Todo(Base):
    id = Column(Integer, primary_key=True)
    name = Column((String(32)), nullable=True)
    phone = Column((String(32)), nullable=False)
    unique_id = Column((String(32)), nullable=False)

