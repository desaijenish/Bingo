from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    name: str
    phone: Optional[str] = None
    unique_id: Optional[str] = None

class TodoCreate(TodoBase):
    name: str
    phone: Optional[str] = None
    unique_id: Optional[str] = None
    

