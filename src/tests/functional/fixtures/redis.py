import aioredis
import pytest_asyncio

from ..settings import settings


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    pool = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT))
    yield pool
    pool.close()
    await pool.wait_closed()


@pytest_asyncio.fixture()
async def clear_redis_cashe(redis_client):
    await redis_client.flushall()
