import json
import os

from elasticsearch import Elasticsearch

from backoff import backoff
from config import logger


class ElasticLoader:
    def __init__(self, host: list, state_key='time'):
        self.client = Elasticsearch(host)
        self.data = []
        self.state_key = state_key

    def read_index_file(self, name_index: str) -> dict:
        index_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'indexes', name_index + '.json')

        with open(index_file_path) as f:
            return json.load(f)

    @backoff()
    def create_index(self, name_index: str) -> None:
        if not self.client.indices.exists(index=name_index):
            index = self.read_index_file(name_index)
            self.client.indices.create(index=name_index, body=index)
            logger.info(f'Создали индекс {name_index}')
        else:
            logger.info(f'Индекс {name_index} уже существует')

    @backoff()
    def bulk_data(self) -> None:
        self.client.bulk(index='movies', body=self.data, refresh=True)

    def load_data_es(self, pg_data: list, index_name: str) -> None:
        for row in pg_data:
            for i in row:
                if row[i] is None:
                    row[i] = []
            self.data.append({"create": {"_index": index_name, "_id": row['uuid']}})
            self.data.append(row)
        self.bulk_data()
        logger.info(f'Данные в Elasticsearch индекс {index_name} загружены')
