import logging
import sys
from time import sleep

from elasticsearch import Elasticsearch

from ..settings import settings

es = Elasticsearch([f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}'], verify_certs=True)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

while True:
    try:
        if not es.ping():
            raise ValueError
    except ValueError:
        logging.log(level=logging.INFO, msg='not connection elasticsearch')
        sleep(10)
    else:
        sys.exit(0)
