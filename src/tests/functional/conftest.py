import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest_asyncio
from multidict import CIMultiDictProxy

from .settings import settings

SERVICE_URL = f'http://{settings.API_HOST}:{settings.API_PORT}'

pytest_plugins = ("tests.functional.fixtures.elastic", "tests.functional.fixtures.redis")


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
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


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
