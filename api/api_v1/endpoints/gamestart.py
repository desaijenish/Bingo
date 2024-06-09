from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Any
from schemas.gamestart import GameStartCreate , GameStartBase , GameBingo
from sqlalchemy.orm import Session
from api import dependencies
from sqlalchemy import func
import crud
import random
import string

router = APIRouter()


@router.get("", status_code=200)
def fetch_all_Game(
    *,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch all game list
    """
    game = crud.gamestart.get(db=db)
    return game



@router.get("/{game_id}", status_code=200)
def fetch_all_game(
    *,
    game_id: int,
    db: Session = Depends(dependencies.get_db),
):
    """
    Fetch game by id
    """
    game = crud.gamestart.get_by_id(db=db, id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"game with ID {game_id} not found")
    return game


@router.post("", status_code=200)
def add_game(
    *,
    game_in: GameStartCreate,
    db: Session = Depends(dependencies.get_db)
) :
    game = crud.gamestart.create(db=db, obj_in=game_in)
    return game



@router.delete("/{game_id}", status_code=200)
def delete_game(*, game_id: int, db: Session = Depends(dependencies.get_db)):
    """
    Delete Game
    """
    result = crud.gamestart.remove(db=db, id=game_id)
    result.status = 0
    db.commit()

    return "game Deleted successfully"


@router.post("/{game_id}/add-bingo-number", response_model=GameStartBase)
def add_bingo_number(
    *,
    game_id: int,
    number: str,
    db: Session = Depends(dependencies.get_db)
):
    """
    Add a number to the bingo array
    """
    game = crud.gamestart.add_bingo_number(db=db, game_id=game_id, number=number)
    return game

@router.post("/gamestart/{game_id}/win")
def set_win(game_id: int, user_id: int, db: Session = Depends(dependencies.get_db)):
    try:
        updated_game = crud.gamestart.set_win(db=db, game_id=game_id, user_id=user_id)
        return {"message": f"Game won by user ID: {updated_game.win_user_id}", "game": updated_game}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)