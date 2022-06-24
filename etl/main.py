import time
from datetime import datetime

import psycopg2
from psycopg2.extras import DictCursor

from backoff import backoff
from config import es_conf, index_names, logger, pg_conf, state_path
from elastic import ElasticLoader
from postgresql import PGLoader
from state import JsonFileStorage, State

elastic_fields = {
    'movies': ('uuid', 'title', 'imdb_rating', 'description',
               'genre', 'actors', 'writers', 'directors'),
    "persons": ('uuid', 'full_name', 'role', 'film_ids'),
    'genres': ('uuid', 'name')
}

batch_size = 1000


@backoff()
def create_index(index_name: str) -> None:
    elastic = ElasticLoader(es_conf)
    elastic.create_index(index_name)


@backoff()
def pg_load_data(index_name: str) -> list:
    with psycopg2.connect(**pg_conf, cursor_factory=DictCursor) as pg_conn:
        db = PGLoader(pg_conn)
        return db.pg_loader(index_name)


@backoff()
def etl(index_name: str) -> None:
    elastic = ElasticLoader(es_conf)
    pg_data = pg_load_data(index_name)
    number_records = len(pg_data)
    logger.info(
        f'Подключились к Postgresql. Записей для загрузки в Elasticsearch индекс {index_name} — {number_records}.'
        )
    index = 0
    batch = []
    while number_records != 0:
        if number_records >= batch_size:
            for row in pg_data[index: index + batch_size]:
                batch.append(dict(zip(elastic_fields[index_name], row)))
                index += 1
            number_records -= batch_size
            elastic.load_data_es(batch, index_name)
        else:
            elastic.load_data_es(
                [
                    dict(zip(elastic_fields[index_name], row))
                    for row in pg_data[index: index + number_records]
                ],
                index_name,
            )
            number_records -= number_records


if __name__ == '__main__':
    for index_name in index_names:
        create_index(index_name)

    while True:
        for index_name in index_names:
            etl(index_name)
        State(JsonFileStorage(state_path)).set_state('time', value=str(datetime.utcnow()))
        time.sleep(30)
