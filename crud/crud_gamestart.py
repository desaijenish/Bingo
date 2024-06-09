from typing import Any, Dict, List, Optional, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.gamestart import GameStart
from models.user import User
from db.base_class import Base
from schemas.gamestart import  GameStartBase ,GameStartCreate
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified

ModelType = TypeVar("ModelType", bound=Base)

class CRUGameStart(CRUDBase[GameStart, GameStartCreate, GameStartBase]):
    def get_by_id(self, db: Session, id: Any) -> GameStart:
        game = db.query(GameStart).filter(GameStart.id == id).first()
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game
    
    def get_user_by_id(self, db: Session, id: Any) -> Optional[User]:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get(self, db: Session) -> Optional[GameStart]:
        return db.query(GameStart).all()
    
    def create(self, db: Session, *, obj_in: GameStart):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: GameStart, obj_in: Union[GameStart, Dict[str, Any]], modified_by=None
    ) -> GameStart:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)



    def remove(self, db: Session, *, id: int):
        obj = db.query(GameStart).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
    def add_bingo_number(self, db: Session, game_id: int, number: str):
        game = self.get_by_id(db, id=game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.win:
            raise HTTPException(status_code=400, detail="Game already won")
        if game.bingo is None:
            game.bingo = []
        if number in game.bingo:
            raise HTTPException(status_code=400, detail="Number already added")
        if len(game.bingo) >= 25:
            raise HTTPException(status_code=400, detail="Bingo is full")

        if int(number) > 25:
            raise HTTPException(status_code=400, detail="Number should not exceed 25")
        if int(number) == 0:
            raise HTTPException(status_code=400, detail="Number should not be 0")

        game.bingo.append(number)
        flag_modified(game, "bingo")
        db.commit()
        db.refresh(game)
        return game
    

    def set_win(self, db: Session, game_id: int, user_id: int) -> GameStart:
        game = self.get_by_id(db, id=game_id)
        user = self.get_user_by_id(db, id=user_id)  # Validate user existence
        
        if game.win:
            raise HTTPException(status_code=400, detail=f"Game already won by user ID: {game.win_user_id}")

        game.win = True
        game.win_user_id = user_id
        flag_modified(game, "win")
        flag_modified(game, "win_user_id")
        db.commit()
        db.refresh(game)
        return game


gamestart = CRUGameStart(GameStart)
