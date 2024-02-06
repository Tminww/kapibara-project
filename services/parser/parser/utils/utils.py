from functools import wraps
import time

import logging


def get_logger(logger_name: str) -> logging:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # создаем обработчик для файла и
    # установим уровень отладки
    ch = logging.FileHandler("./parser/log/parser.log", "a")
    # ch.setLevel(logging.DEBUG)

    # строка формата сообщения
    strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
    # строка формата времени
    datefmt = "%Y-%m-%d %H:%M:%S"
    # создаем форматтер
    formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

    # добавляем форматтер к 'ch'
    ch.setFormatter(formatter)
    # добавляем ch в регистратор
    logger.addHandler(ch)
    # вызов функций, регистрирующих
    # события в коде
    return logger  # type: ignore


def check_time(logger):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            output = func(*args, **kwargs)
            end_time = time.time()
            logger.info(
                f"Функция {func.__name__} затратила времени: {end_time - start_time} секунд"
            )
            return output

        return wrapper

    return decorate


def retry(logger, exception_to_check, num_retries=5, sleep_time=1):
    """
    Decorator that retries the execution of a function if it raises a specific exception.
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for retry in range(1, num_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    logger.error(
                        f"{func.__name__} вернула ошибку {e.__class__.__name__}. {retry} попытка..."
                    )
                    if retry < num_retries:
                        time.sleep(sleep_time)
            # Raise the exception if the function was not successful after the specified number of retries
            logger.error(f"{func.__name__} завершилась с ошибкой")

        return wrapper

    return decorate
