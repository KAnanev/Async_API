from typing import List, Optional

from pydantic import BaseModel

from models.base import MoviesBaseModel


class Genre(MoviesBaseModel):
    name: str
    description: Optional[str] = ''


class GenreList(BaseModel):
    __root__: List[Genre]
