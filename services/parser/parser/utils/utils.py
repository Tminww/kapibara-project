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
                        f"status: {status}, \nresponse: {response}, \nerror: {error} \n{retry} попытка..."
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


def response_status(response):
    status = True
    if response.status_code != 200:
        status = False
    return {"status": status, "code": response.status_code, "reason": response.reason}


def get_response(url):
    s = requests.Session()
    user = fake_useragent.UserAgent().random
    header = {"user-agent": user}
    response = s.get(url, headers=header)
    logging.info(f"{url}, {res.status_code}, {s.cookies}")
    return response


def try_request(req):
    def wrap(url):
        status = False
        try:
            response = req(url)
            error = 0
            status = True
        except Exception as ex:
            response = Response()
            response.reason = ex
            response.status_code = 444
            error = sys.exc_info()[1]
        return {"status": status, "response": response, "error": error}

    return wrap
