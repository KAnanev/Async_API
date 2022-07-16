import logging
import sys
from time import sleep

from redis import Redis
from redis.exceptions import ConnectionError

from ..settings import settings

redis = Redis(settings.REDIS_HOST)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

while True:
    try:
        redis.ping()
    except ConnectionError:
        logging.log(level=logging.INFO, msg='not connection redis')
        sleep(10)
    else:
        sys.exit(0)
