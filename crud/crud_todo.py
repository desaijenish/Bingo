from typing import Any, Dict, List, Optional, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.todo import Todo
from db.base_class import Base
from schemas.todo import TodoCreate, TodoBase

ModelType = TypeVar("ModelType", bound=Base)

class CRUDTodo(CRUDBase[Todo, TodoCreate, TodoBase]):
    def get_by_id(self, db: Session, id: Any) -> Optional[Todo]:
        return db.query(Todo).filter(Todo.id == id).first()

    def get(self, db: Session) -> Optional[Todo]:
        return db.query(Todo).all()

    def create(self, db: Session, *, obj_in: TodoCreate):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Todo, obj_in: Union[Todo, Dict[str, Any]], modified_by=None
    ) -> Todo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)



    def remove(self, db: Session, *, id: int) -> Todo:
        obj = db.query(Todo).get(id)
        db.delete(obj)
        db.commit()
        return obj

todo = CRUDTodo(Todo)
