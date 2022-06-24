import time
from functools import wraps

from config import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=30):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 1
            sleep_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.exception('Ошибка соединения')
                    sleep_time = sleep_time * factor ** n
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
                    n += 1
                    logger.info(f'Пробуем подключаться раз в {sleep_time} секунд')
                    time.sleep(sleep_time)
        return inner
    return func_wrapper
