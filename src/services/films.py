from functools import lru_cache

from db.base import AsyncCacheStorage, AsyncStorage
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.film import Film, FilmList

from services.base import BaseService


class FilmService(BaseService):
    elastic_index_name = 'movies'
    model = Film
    model_lists = FilmList
    fields = {'title': 5, 'actors': 3, 'description': 1}


@lru_cache()
def get_film_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        storage: AsyncStorage = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, storage)
