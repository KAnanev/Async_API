from typing import List, Optional

from pydantic import BaseModel

from models.base import MoviesBaseModel


class Film(MoviesBaseModel):
    title: str
    imdb_rating: float = 0.0
    description: Optional[str] = ''
    genre: List[dict]  = [{}]
    actors: List[dict] = [{}]
    writers: List[dict] = [{}]
    directors: List[dict] = [{}]


class FilmList(BaseModel):
    __root__: List[Film]
