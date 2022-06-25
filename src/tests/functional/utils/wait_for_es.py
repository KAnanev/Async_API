import sys
import logging
from time import sleep

from elasticsearch import Elasticsearch

es = Elasticsearch(['elasticsearch:9200'], verify_certs=True)
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
