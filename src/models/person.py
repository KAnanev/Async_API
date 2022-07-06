from typing import List

from pydantic import BaseModel

from models.base import MoviesBaseModel


class Person(MoviesBaseModel):
    full_name: str


class PersonList(BaseModel):
    __root__: List[Person]
