import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from ..settings import settings
from ..test_data import (genres_data, genres_index, movies_data, movies_index,
                         persons_data, persons_index)
from ..utils.es_loader import delete_index, load_data_es


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}')
    yield client
    await client.close()


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
