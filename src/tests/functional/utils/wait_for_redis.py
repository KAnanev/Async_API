import sys

from redis import Redis

from ..settings import settings
from .backoff import backoff


@backoff('redis')
def connect_to_redis():
    redis = Redis(settings.REDIS_HOST)
    redis.ping()
    sys.exit(0)


if __name__ == "__main__":
    connect_to_redis()
