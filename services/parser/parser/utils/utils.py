import time
from parser.log.createLogger import get_logger


logging = get_logger("utils.utils")


def check_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        logging.info(
            f"Функция {func.__name__} затратила времени: {end_time - start_time} секунд"
        )
        return res

    return wrapper
