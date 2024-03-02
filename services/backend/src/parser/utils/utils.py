from functools import wraps
import sys
import time

import logging

from requests import Response


def get_logger(logger_name: str) -> logging:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # создаем обработчик для файла и
    # установим уровень отладки
    ch = logging.FileHandler("./src/parser/logging/parser.log", "a")
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


def retry_request(logger, num_retries=5, sleep_time=1):
    """
    Decorator that retries the execution of a function if it raises a specific exception.
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            status = False
            for retry in range(1, num_retries + 1):
                try:
                    response = func(*args, **kwargs)
                    error = 0
                    status = True

                    logger.debug(
                        f'status: {status}, url: {response.url} response: {response}, error: {error}"'
                    )
                    return {"status": status, "response": response, "error": error}
                except Exception as exception:
                    response = Response()
                    response.reason = exception
                    response.status_code = 444
                    error = sys.exc_info()[1]
                    logger.error(
                        f"status: {status}, response: {response}, error: {error} {retry} попытка..."
                    )
                    if retry < num_retries:
                        time.sleep(sleep_time)

            # logger.error(f"{func.__name__} завершилась с ошибкой")
            logger.debug(
                f'status: {status}, url: {response.url} response: {response}, error: {error}"'
            )

            return {"status": status, "response": response, "error": error}

            # Raise the exception if the function was not successful after the specified number of retries

        return wrapper

    return decorate


def compare_regions(mock_regions, api_regions) -> tuple:
    mock_regions_name = [region["name"] for region in mock_regions]

    for region in api_regions:
        if region["name"] not in mock_regions_name:
            error = region["name"]
            return (False, error)
    return (True, None)


def get_row(table: str, column: list, where: dict):

    columns = ",".join(column)

    where_params = [f"{pair} = '{where.get(pair)}'" for pair in where.keys]

    # cursor.execute(f"SELECT {columns} from {table} WHERE {where_params};")
    # answer = cursor
    # return answer
    # logger.debug(f"SELECT {columns} from {table} WHERE {where_params};")
    print(f"SELECT {columns} from {table} WHERE {where_params};")
    return f"SELECT {columns} from {table} WHERE {where_params};"
