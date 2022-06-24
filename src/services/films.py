from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, FilmList
from services.base import BaseService


class FilmService(BaseService):
    elastic_index_name = 'movies'
    model = Film
    model_lists = FilmList
    fields = {'title': 5, 'actors': 3, 'description': 1}


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
