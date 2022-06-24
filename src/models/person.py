from datetime import date
from typing import Optional, List

from pydantic import BaseModel

from models.base import MoviesBaseModel


class Person(MoviesBaseModel):
    full_name: str
    birth_date: Optional[date]


class PersonList(BaseModel):
    __root__: List[Person]
