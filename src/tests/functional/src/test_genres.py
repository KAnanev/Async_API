import asyncio
import random
from uuid import uuid4

import pytest

from ..test_data.genres_data import GENRES


@pytest.mark.asyncio
async def test_random_existent_genre(load_genres_data, make_get_request):
    random_genre = GENRES[random.randint(0, len(GENRES)-1)]

    response = await make_get_request(f'/genres/{random_genre["uuid"]}')

    assert response.status == 200
    assert response.body == random_genre


@pytest.mark.asyncio
async def test_random_nonexistent_genre(load_genres_data, make_get_request):
    nonexistent_genre_id = uuid4()

    response = await make_get_request(f'/genres/{nonexistent_genre_id}')

    assert response.status == 404
    assert len(response.body) == 1
    assert response.body == {"detail": "Genre not found"}


@pytest.mark.asyncio
async def test_genres_query_params_type_error(load_genres_data, make_get_request):
    response = await make_get_request('/genres/', {"from": "f", "size": "s", "page": "k"})

    assert response.status == 422
    assert response.body == {"detail": [
        {"loc": ["query", "from"], "msg":"value is not a valid integer", "type": "type_error.integer"},
        {"loc": ["query", "size"], "msg":"value is not a valid integer", "type": "type_error.integer"},
        {"loc": ["query", "page"], "msg":"value is not a valid integer", "type": "type_error.integer"}
        ]}


@pytest.mark.asyncio
async def test_genres_search(load_genres_data, make_get_request):
    genre_to_find = [genre for genre in GENRES if genre['uuid'] == '0b105f87-e0a5-45dc-8ce7-f8632088f390']
    await asyncio.sleep(1)

    response = await make_get_request('/genres/', {'query': 'Western'})

    assert response.status == 200
    assert response.body != []
    assert response.body == genre_to_find


@pytest.mark.asyncio
async def test_genres_endpoint(load_genres_data, make_get_request):
    await asyncio.sleep(1)
    response = await make_get_request('/genres/?size=50')

    assert response.status == 200
    assert len(response.body) == len(GENRES)
    assert response.body == GENRES
