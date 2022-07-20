import types
from collections import defaultdict
from typing import List, Optional, Union

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.film import Film, FilmList
from models.genre import Genre, GenreList
from models.person import Person, PersonList

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

MAP_SORT_ES = types.MappingProxyType(
    {
        'imdb_rating': 'imdb_rating',
    }
)


def get_sort_for_es(sort_value: str) -> List[dict]:
    sorter = 'asc'
    result = None
    if value := MAP_SORT_ES.get(sort_value.lstrip('-')):
        if sort_value.startswith('-'):
            sorter = 'desc'
        result = [
            {
                value: sorter
            }
        ]
    return result


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    def elastic_index_name(self) -> str:
        pass

    def model(*args, **kwargs) -> Union[Film, Person, Genre]:
        pass

    def model_lists(*args, **kwargs) -> Union[FilmList, PersonList, GenreList]:
        pass

    def fields(self) -> dict:
        pass

    async def _put_item_to_cache(self, item: Union[Film, Person, Genre]):
        await self.redis.set(
            str(item.uuid), item.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_from_cache(
            self, item_id: str
    ) -> Optional[Union[Film, Person, Genre]]:
        redis_data = await self.redis.get(item_id)
        if not redis_data:
            return None
        item = self.model.parse_raw(redis_data)
        return item

    async def _put_items_to_cache(
            self,
            key_redis: str, items: Union[FilmList, PersonList, GenreList]):
        await self.redis.set(
            key_redis, items.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_items_from_cache(
            self,
            key_redis: str
    ) -> Optional[Union[FilmList, PersonList, GenreList]]:
        redis_data = await self.redis.get(key_redis)
        if not redis_data:
            return None
        item = self.model_lists.parse_raw(redis_data)
        return item

    async def _get_item_from_elastic(
            self,
            item_id: str) -> Optional[Union[Film, Person, Genre]]:
        try:
            item = await self.elastic.get(self.elastic_index_name, item_id)
        except NotFoundError:
            return None
        return self.model(**item['_source'])

    async def get_by_id(
            self,
            item_id: str) -> Optional[Union[Film, Person, Genre]]:
        item = await self._get_from_cache(str(item_id))
        if not item:
            item = await self._get_item_from_elastic(str(item_id))
            if not item:
                return None
            await self._put_item_to_cache(item)
        return item

    async def get_all_items(self, params: Optional[dict]):

        key_redis = 'Movies:{service}: sort={sort}, query={query}, page_number={page},\
            page_size={size}'.format(**params)
        items = await self._get_items_from_cache(key_redis)

        if not items:

            body = defaultdict(lambda: defaultdict(dict))

            body['from'] = (params['page'] * params['size']) - params['size']
            body['size'] = params['size']

            if params['sort']:
                if sort_value := get_sort_for_es(params['sort']):
                    body['sort'] = sort_value

            if params['query']:
                body['query']['bool']['should'] = []
                for field, weight in self.fields.items():
                    match = defaultdict(lambda: defaultdict(dict))
                    match['match'][field]['query'] = params['query']
                    match['match'][field]['boost'] = weight
                    body['query']['bool']['should'].append(match)
            else:
                body['query']['match_all'] = {}

            items = await self.elastic.search(
                index=self.elastic_index_name,
                body=body
            )

            if not items:
                return None

            items = map(
                lambda item: {'id': item['_id'], **item['_source']},
                items.get('hits', {}).get('hits', [])
            )

            items = self.model_lists.parse_obj(list(items))
            await self._put_items_to_cache(key_redis, items)
        return items
