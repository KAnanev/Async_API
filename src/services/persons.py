from functools import lru_cache

from fastapi import Depends

from db.base import AsyncCacheStorage, AsyncStorage
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
        cache: AsyncCacheStorage = Depends(get_redis),
        storage: AsyncStorage = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, storage)
