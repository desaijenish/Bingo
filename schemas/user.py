from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: Optional[str] = None
    unique_id: int = 1


class UserCreate(UserBase):
    name: Optional[str] = None
    unique_id: int = 1

class UserGeneratedCode(BaseModel):
    generated_code: Optional[str] = None

class UserAddCode(BaseModel):
    add_code: Optional[str] = None

