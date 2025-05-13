from functools import wraps
import json

from fastapi import Request


def cache_response(backend, ttl: int = 3600):
    """
    Декоратор для кэширования ответов API в Redis.

    Args:
        ttl (int): Время жизни кэша в секундах (по умолчанию 1 час).
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Извлекаем объект Request из аргументов
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            if request is None:
                request = kwargs.get("request")

            if request is None:
                raise ValueError("Объект Request не найден в аргументах функции")

            # Формируем уникальный ключ кэша на основе пути и параметров запроса
            cache_key = f"{request.url.path}:{json.dumps(dict(request.query_params), sort_keys=True)}"

            # Проверяем наличие данных в кэше
            cached_data = backend.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

            # Выполняем оригинальную функцию, если данных в кэше нет
            result = await func(*args, **kwargs)

            # Сохраняем результат в кэш с заданным временем жизни
            backend.setex(cache_key, ttl, json.dumps(result.dict()))
            return result

        return wrapper

    return decorator
