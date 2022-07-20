from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.v1.base import item_details, item_list, PaginatedParams
from models.person import Person, PersonList
from services.persons import PersonService, get_person_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
        ) -> Person:
    item = await item_details(person_id, person_service)
    return item


@router.get('/', response_model=PersonList)
async def person_list(
        person_service: PersonService = Depends(get_person_service),
        sort_: Optional[str] = Query(None, title='Сортировка', alias='sort'),
        query_: Optional[str] = Query(None, title='Поисковый запрос', alias='query'),
        page_: Optional[int] = Query(PaginatedParams().page_number, title='№ страницы', alias='page'),
        size_: Optional[int] = Query(PaginatedParams().page_size, title='Cколько выдать', alias='size'),
) -> PersonList:
    """
        Список жанров с постраничной навигацией и поисковым запросом:
        _http://0.0.0.0:8000/api/v1/genres/?from=0&size=10&query=query&page=1_

        - **sort_**: Сортировка.
        - **query_**: Поисковый запрос.
        - **page_**: № страницы.
        - **size_**: Cколько выдать.

    """

    params = {'sort': sort_, 'query': query_, 'page': page_, 'size': size_,}

    persons = await item_list(service=person_service, params=params)
    return persons
