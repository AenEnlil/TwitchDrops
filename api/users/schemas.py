from typing import List

from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    user_id: int


class GameSchema(BaseModel):
    game: str


class UserGamesSubscribeSchema(BaseModel):
    games: List[GameSchema]
