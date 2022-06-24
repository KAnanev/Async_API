import logging

import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis

description = """
    Movies API, получаем данные по фильмам. 🚀
    
    ## Films
    Данные по фильмам.

    ## Genres
    Данные по жанрам
    
    ## Persons
    Данные по участникам фильма.
"""

tags_metadata = [
    {
        "name": "films",
        "description": """Получение фильма по ID и список фильмов по странично, 
        можно использовать поисковый запрос.""",
    },
    {
        "name": "genres",
        "description": """Получение жанра по ID и список жанров по странично, 
        можно использовать поисковый запрос.""",
    },
    {
        "name": "persons",
        "description": """Получение участника фильма по ID и список участников по странично, 
        можно использовать поисковый запрос.""",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
)


@app.on_event('startup')
async def startup():
    try:
        redis.redis = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20)
    except ConnectionRefusedError:
        quit('Redis don\'t work!!!')
    elastic.es = AsyncElasticsearch(hosts=[f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
