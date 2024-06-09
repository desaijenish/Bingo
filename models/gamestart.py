from sqlalchemy import Column, Integer, ForeignKey, ARRAY, String, Boolean
from db.base_class import Base

class GameStart(Base):
    id = Column(Integer, primary_key=True, index=True)
    generated_user_id = Column(Integer, ForeignKey("user.id"))
    add_user_id = Column(Integer, ForeignKey("user.id"))
    bingo = Column(ARRAY(String), nullable=True, default=[])  # Ensure default is an empty list
    win = Column(Boolean, nullable=False, default=False)
    win_user_id = Column(Integer, ForeignKey("user.id") , nullable=True)
