from functools import lru_cache

from db.base import AsyncCacheStorage, AsyncStorage
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.genre import Genre, GenreList

from services.base import BaseService


class GenreService(BaseService):
    elastic_index_name = 'genres'
    model = Genre
    model_lists = GenreList
    fields = {'name': 3}


@lru_cache()
def get_genre_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        storage: AsyncStorage = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, storage)
