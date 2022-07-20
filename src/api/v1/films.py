from typing import Optional

from api.v1.base import PaginatedParams, item_details, item_list
from fastapi import APIRouter, Depends, Query
from models.film import Film, FilmList
from services.films import FilmService, get_film_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/{film_id}', response_model=Film)
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
        ) -> Film:
    """
        Информация по фильму:

         - **film_id**: ID фильма.
    """
    item = await item_details(film_id, film_service)
    return item


@router.get('/', response_model=FilmList)
async def film_list(
        film_service: FilmService = Depends(get_film_service),
        sort_: Optional[str] = Query(None, title='Сортировка', alias='sort'),
        query_: Optional[str] = Query(None, title='Поисковый запрос', alias='query'),
        page_: Optional[int] = Query(PaginatedParams().page_number, title='№ страницы', alias='page'),
        size_: Optional[int] = Query(PaginatedParams().page_size, title='Cколько выдать', alias='size'),
) -> FilmList:
    """
        Список фильмов с сортировкой по рейтингу IMDB по убыванию, постраничной навигацией и поисковым запросом:
        http://0.0.0.0:8000/api/v1/films/?sort=-imdb_rating&query=Endor&page=1&size=10

        - **sort**: Сортировка.
        - **query**: Поисковый запрос.
        - **page**: № страницы.
        - **size**: Cколько выдать.
    """

    params = {'sort': sort_, 'query': query_, 'page': page_, 'size': size_}

    films = await item_list(service=film_service, params=params)
    return films
