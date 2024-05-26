from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from schemas.todo import TodoBase, TodoCreate
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user

router = APIRouter()


@router.get("/", status_code=200)
def fetch_all_users(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all users list
    """
    todo = crud.todo.get(db=db)
    return todo



@router.get("/{todo_id}", status_code=200)
def fetch_all_users(
    *,
    todo_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch users by id
    """
    todo = crud.todo.get_by_id(db=db, id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with ID {todo_id} not found")
    return todo


@router.post("", status_code=200)
def add_user(
    *,
    todo_in: TodoCreate,
    db: Session = Depends(dependencies.get_db)
) :
    todo = crud.todo.create(db=db, obj_in=todo_in)
    return todo

@router.put("/{todo_id}", status_code=200)
def update_todo(
    *,
    db: Session = Depends(dependencies.get_db),
    todo_id: int,
    todo_in: TodoCreate
):
    todo_item = crud.todo.get_by_id(db=db, id=todo_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo not found")
    return crud.todo.update(db=db, db_obj=todo_item, obj_in=todo_in)


@router.delete("/{todo_id}", status_code=200)
def delete_user(*, todo_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete User
    """
    result = crud.todo.remove(db=db, id=todo_id)
    result.status = 0
    db.commit()

    return "User Deleted successfully"
