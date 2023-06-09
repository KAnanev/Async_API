import asyncio
import random
from http import HTTPStatus
from operator import itemgetter
from uuid import uuid4

import pytest

from ..test_data.movies_data import MOVIES
from ..utils.es_loader import delete_index


@pytest.mark.asyncio
async def test_random_existent_film(load_movies_data, make_get_request, clear_redis_cashe):
    random_film = MOVIES[random.randint(0, len(MOVIES)-1)]

    response = await make_get_request(f'/films/{random_film["uuid"]}')

    assert response.status == HTTPStatus.OK
    assert response.body == random_film


@pytest.mark.asyncio
async def test_random_nonexistent_film(load_movies_data, make_get_request):
    nonexistent_film_id = uuid4()

    response = await make_get_request(f'/films/{nonexistent_film_id}')

    assert response.status == HTTPStatus.NOT_FOUND
    assert len(response.body) == 1
    assert response.body == {"detail": "Film not found"}


@pytest.mark.asyncio
async def test_films_query_params_type_error(load_movies_data, make_get_request):
    response = await make_get_request('/films/', {"page": "p", "size": "s"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body == {"detail": [
        {"loc": ["query", "page"], "msg":"value is not a valid integer", "type": "type_error.integer"},
        {"loc": ["query", "size"], "msg":"value is not a valid integer", "type": "type_error.integer"}
        ]}


@pytest.mark.asyncio
async def test_films_sorting_imdb(load_movies_data, make_get_request):
    sorted_films = sorted(MOVIES, key=itemgetter('imdb_rating'), reverse=True)
    await asyncio.sleep(1)

    response = await make_get_request('/films/', {'sort': '-imdb_rating'})

    assert response.status == HTTPStatus.OK
    assert response.body == sorted_films


@pytest.mark.asyncio
async def test_films_search(load_movies_data, make_get_request):
    film_to_find = [film for film in MOVIES if film['uuid'] == 'ee580283-32db-4181-9f11-bd9d171944c3']
    await asyncio.sleep(1)

    response = await make_get_request('/films/', {'query': 'Endor'})

    assert response.status == HTTPStatus.OK
    assert response.body != []
    assert response.body == film_to_find


@pytest.mark.asyncio
async def test_films_endpoint(load_movies_data, make_get_request):
    await asyncio.sleep(1)
    response = await make_get_request('/films/', {})

    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(MOVIES)
    assert response.body == MOVIES


@pytest.mark.asyncio
async def test_cache_without_index(es_client, clear_redis_cashe, make_get_request):
    random_film = MOVIES[random.randint(0, len(MOVIES)-1)]

    response_from_elastic = await make_get_request(f'/films/{random_film["uuid"]}')
    await delete_index(es_client, 'movies')

    response_from_redis = await make_get_request(f'/films/{random_film["uuid"]}')

    assert response_from_elastic.status == HTTPStatus.OK
    assert response_from_redis.status == HTTPStatus.OK
    assert response_from_elastic.body == response_from_redis.body == random_film
