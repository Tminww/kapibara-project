from functools import wraps
import time
from typing import Annotated, Awaitable
from httpx import AsyncClient, Response
from tenacity import retry, stop_after_attempt, wait_fixed


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


@retry(
    stop=stop_after_attempt(3), wait=wait_fixed(10)
)  # 3 попытки с интервалом 2 секунды
async def fetch(client: AsyncClient, url, params: dict = None) -> Response:
    print(url, params)
    return await client.get(url, params=params)
