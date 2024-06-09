from typing import Any, Dict, List, Optional, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.user import User
from db.base_class import Base
from schemas.user import UserCreate, UserBase

ModelType = TypeVar("ModelType", bound=Base)

class CRUDUser(CRUDBase[User, UserCreate, UserBase]):
    def get_by_id(self, db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get(self, db: Session) -> Optional[User]:
        return db.query(User).all()
    
    def get_by_generated_code(self, db: Session, generated_code: str) -> Optional[User]:
        return db.query(User).filter(User.generated_code == generated_code).first()
    
    def get_by_unique_id(db: Session, unique_id: Any):
        return db.query(User).filter(User.unique_id == unique_id).first()

    def create(self, db: Session, *, obj_in: UserCreate):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[User, Dict[str, Any]], modified_by=None
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)



    def remove(self, db: Session, *, id: int) -> User:
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj

user = CRUDUser(User)
