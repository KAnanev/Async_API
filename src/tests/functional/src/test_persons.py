import asyncio
import random
from uuid import uuid4

import pytest
from test_data.persons_data import PERSONS


@pytest.mark.asyncio
async def test_random_existent_person(load_persons_data, make_get_request):
    random_person = PERSONS[random.randint(0, len(PERSONS)-1)]

    response = await make_get_request(f'/persons/{random_person["uuid"]}')

    assert response.status == 200
    assert response.body == random_person


@pytest.mark.asyncio
async def test_random_nonexistent_person(load_persons_data, make_get_request):
    nonexistent_person_id = uuid4()

    response = await make_get_request(f'/persons/{nonexistent_person_id}')

    assert response.status == 404
    assert len(response.body) == 1
    assert response.body == {"detail": "Person not found"}


@pytest.mark.asyncio
async def test_persons_query_params_type_error(load_persons_data, make_get_request):
    response = await make_get_request('/persons/', {"from": "f", "size": "s", "page": "k"})

    assert response.status == 422
    assert response.body == {"detail": [
        {"loc": ["query", "from"], "msg":"value is not a valid integer", "type": "type_error.integer"},
        {"loc": ["query", "size"], "msg":"value is not a valid integer", "type": "type_error.integer"},
        {"loc": ["query", "page"], "msg":"value is not a valid integer", "type": "type_error.integer"}
        ]}


# @pytest.mark.asyncio
# async def test_persons_search(load_persons_data, make_get_request):
#     person_to_find = [person for person in PERSONS if person['uuid'] == '3214cf58-8dbf-40ab-9185-77213933507e']
#     await asyncio.sleep(1)

#     response = await make_get_request('/persons/', {'query': 'Marquand'})

#     assert response.status == 200
#     assert response.body != []
#     assert response.body == person_to_find


@pytest.mark.asyncio
async def test_persons_endpoint(load_persons_data, make_get_request):
    await asyncio.sleep(1)
    response = await make_get_request('/persons/?size=50')

    assert response.status == 200
    assert len(response.body) == len(PERSONS)
    assert response.body == PERSONS
