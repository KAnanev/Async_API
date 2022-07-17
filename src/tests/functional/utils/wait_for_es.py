import sys

from elasticsearch import Elasticsearch

from ..settings import settings
from .backoff import backoff


@backoff('elasticsearch')
def connect_to_elasticsearch():
    es = Elasticsearch([f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'], verify_certs=True)
    if not es.ping():
        raise ConnectionError
    sys.exit(0)


if __name__ == "__main__":
    connect_to_elasticsearch()
