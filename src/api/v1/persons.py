from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.v1.base import item_details, item_list
from models.person import Person, PersonList
from services.persons import PersonService, get_person_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/{person_id}', response_model=Person)
async def person_details(
        person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    item = await item_details(person_id, person_service)
    return item


@router.get('/', response_model=PersonList)
async def person_list(person_service: PersonService = Depends(get_person_service),
                      from_: Optional[int] = Query(0, title='Начало выдачи', alias='from'),
                      size_: Optional[int] = Query(10, title='Cколько выдать', alias='size'),
                      query_: Optional[str] = Query(None, title='Поисковый запрос', alias='query'),
                      page_: Optional[int] = Query(1, title='№ страницы', alias='page'), ) -> PersonList:
    """
        Список участников фильма с постраничной навигацией и поисковым запросом:
        _http://0.0.0.0:8000/api/v1/persons/?from=0&size=10&query=query&page=1_

        - **from_**: Начало выдачи.
        - **size_**: Cколько выдать.
        - **query_**: Поисковый запрос.
        - **page_**: № страницы.
    """

    params = {'from': from_, 'size': size_, 'page': page_, 'query': query_}

    persons = await item_list(service=person_service, params=params)
    return persons
