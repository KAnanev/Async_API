from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person, PersonList
from services.base import BaseService


class PersonService(BaseService):
    elastic_index_name = 'persons'
    model = Person
    model_lists = PersonList
    fields = {'last_name': 5, 'first_name': 3}


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
