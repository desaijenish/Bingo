from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from schemas.user import UserBase, UserCreate ,UserGeneratedCode , UserAddCode
from schemas.gamestart import GameStartCreate
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
from util.user_util import get_current_user
import random
import string


router = APIRouter()


@router.get("", status_code=200)
def fetch_all_users(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all users list
    """
    user = crud.user.get(db=db)
    return user



@router.get("/{user_id}", status_code=200)
def fetch_all_users(
    *,
    user_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch users by id
    """
    user = crud.user.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with ID {user_id} not found")
    return user


@router.post("", status_code=200)
def add_user(
    *,
    user_in: UserCreate,
    db: Session = Depends(dependencies.get_db)
) :
    user = crud.user.create(db=db, obj_in=user_in)
    return user

@router.put("/{user_id}", status_code=200)
def update_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: UserCreate
):
    user_item = crud.user.get_by_id(db=db, id=user_id)
    if not user_item:
        raise HTTPException(status_code=404, detail="user not found")
    return crud.user.update(db=db, db_obj=user_item, obj_in=user_in)


@router.delete("/{user_id}", status_code=200)
def delete_user(*, user_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete User
    """
    result = crud.user.remove(db=db, id=user_id)
    result.status = 0
    db.commit()

    return "User Deleted successfully"

@router.post("/users/{user_id}/generate-code/", response_model=UserGeneratedCode)
def generate_code_for_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    db_user = crud.user.get_by_id(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    random_code = ''.join(random.choices(string.digits, k=6))

    db_user.generated_code = random_code
    db_user.add_code = None
    db.commit()

    return {"generated_code": random_code}

@router.post("/users/{user_id}/add-code/", response_model=int)
def add_code_to_user(user_id: int, add_code: str, db: Session = Depends(dependencies.get_db)):
    receiving_user = crud.user.get_by_id(db=db, id=user_id)
    if receiving_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    receiving_user.add_code = add_code
    receiving_user.generated_code = None
    db.commit()

    matching_user = crud.user.get_by_generated_code(db=db, generated_code=add_code)
    if matching_user is None:
        raise HTTPException(status_code=404, detail="Matching user not found")

    game_data = GameStartCreate(
        generated_user_id=receiving_user.id,
        add_user_id=matching_user.id,
        bingo=[],  
        win=False
    )

    game_start = crud.gamestart.create(db=db, obj_in=game_data)

    return game_start.id

