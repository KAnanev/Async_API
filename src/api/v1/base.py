from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from models.film import Film, FilmList
from models.genre import Genre, GenreList
from models.person import Person, PersonList
from services.films import FilmService
from services.genres import GenreService
from services.persons import PersonService


async def item_details(
        item_id: str,
        service: Union[FilmService, GenreService, PersonService]
        ) -> Union[Film, Person, Genre]:
    """Базовый detail запрос."""
    item = await service.get_by_id(item_id)

    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='{0} not found'.format(service.model.__name__))

    return item


async def item_list(
        service: Union[FilmService, GenreService, PersonService],
        params: dict
        ) -> Union[FilmList, GenreList, PersonList]:

    params['service'] = service.model.__name__
    items = await service.get_all_items(params=params)

    return items
