import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import settings
from .test_data import (genres_data, genres_index, movies_data, movies_index,
                        persons_data, persons_index)
from .utils.es_loader import delete_index, load_data_es

SERVICE_URL = f'http://{settings.API_HOST}:{settings.API_PORT}'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}')
    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    pool = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT))
    yield pool
    pool.close()
    await pool.wait_closed()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture()
async def clear_redis_cashe(redis_client):
    await redis_client.flushall()


@pytest_asyncio.fixture(scope='session')
async def load_genres_data(es_client):
    await load_data_es(es_client, 'genres', genres_index.INDEX, genres_data.GENRES)
    yield
    await delete_index(es_client, 'genres')


@pytest_asyncio.fixture(scope='session')
async def load_movies_data(es_client):
    await load_data_es(es_client, 'movies', movies_index.INDEX, movies_data.MOVIES)
    yield
    await delete_index(es_client, 'movies')


@pytest_asyncio.fixture(scope='session')
async def load_persons_data(es_client):
    await load_data_es(es_client, 'persons', persons_index.INDEX, persons_data.PERSONS)
    yield
    await delete_index(es_client, 'persons')


@pytest_asyncio.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + f'/api/{settings.API_VERSION}' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
                )
    return inner
