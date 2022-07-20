from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.v1.base import item_details, item_list, PaginatedParams
from models.genre import Genre, GenreList
from services.genres import GenreService, get_genre_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
        Информация по жанру:

        - **genre_id**: ID жанра.
    """
    item = await item_details(genre_id, genre_service)
    return item


@router.get('/', response_model=GenreList)
async def genre_list(
        genre_service: GenreService = Depends(get_genre_service),
        sort_: Optional[str] = Query(None, title='Сортировка', alias='sort'),
        query_: Optional[str] = Query(None, title='Поисковый запрос', alias='query'),
        page_: Optional[int] = Query(PaginatedParams().page_number, title='№ страницы', alias='page'),
        size_: Optional[int] = Query(PaginatedParams().page_size, title='Cколько выдать', alias='size'),
) -> GenreList:
    """
        Список жанров с постраничной навигацией и поисковым запросом:
        _http://0.0.0.0:8000/api/v1/genres/?from=0&size=10&query=query&page=1_

        - **sort_**: Сортировка.
        - **query_**: Поисковый запрос.
        - **page_**: № страницы.
        - **size_**: Cколько выдать.

    """
    params = {'sort': sort_, 'query': query_, 'page': page_, 'size': size_,}

    genres = await item_list(service=genre_service, params=params)
    return genres
