from typing import List, Optional
from pydantic import BaseModel

class GameStartBase(BaseModel):
    generated_user_id:int
    add_user_id:int
    bingo: Optional[List[str]] = None
    win: bool = False

class GameStartCreate(GameStartBase):
    pass

class GameBingo(BaseModel):
    bingo: List[str]
