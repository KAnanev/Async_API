import logging
import sys
import time
from functools import wraps

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def backoff(name_service, start_sleep_time=0.1, factor=2, border_sleep_time=30,):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 1
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logging.log(
                        level=logging.FATAL, msg=f'Not connection {name_service}')
                    sleep_time = sleep_time * factor ** n
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
                    n += 1
                    logging.log(
                        level=logging.INFO, msg=f'Пробуем подключаться к {name_service} раз в {sleep_time} секунд')
                    time.sleep(sleep_time)
        return inner
    return func_wrapper
