from abc import ABC, abstractmethod
import httpx
import fake_useragent
from src.schemas.retry_request import RetryRequestSchema
from src.utils import utils


logger = utils.get_logger(logger_name="http_external_requests", file_name="http")


class IHttpClient(ABC):
    @abstractmethod
    async def get(self, path: str, payload: dict = None) -> RetryRequestSchema:
        raise NotImplementedError


class HttpClient(IHttpClient):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        user = fake_useragent.UserAgent().random
        self.headers = {"user-agent": user}

    @utils.async_retry_request(logger=logger)
    async def get(self, path: str, payload: dict = None) -> RetryRequestSchema:
        try:
            # Используем асинхронный httpx.AsyncClient
            async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=60) as client:
                response = await client.get(url=path, params=payload)

                # Логгируем успешный ответ
                logger.info(f"URL: {response.url}, Status code: {response.status_code}")

                return response

        except Exception as e:
            logger.error(f"Ошибка при выполнении GET запроса: {e}")
            raise e
