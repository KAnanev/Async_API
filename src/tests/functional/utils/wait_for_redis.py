import sys
import logging
from time import sleep

from redis import Redis
from redis.exceptions import ConnectionError

redis = Redis('redis')
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

while True:
    try:
        redis.ping()
    except ConnectionError:
        logging.log(level=logging.INFO, msg='not connection redis')
        sleep(10)
    else:
        sys.exit(0)
