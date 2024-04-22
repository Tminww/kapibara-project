from abc import ABC, abstractmethod
import requests
from schemas.retry_request import RetryRequestSchema
from utils import utils
import fake_useragent

import aiohttp


logger = utils.get_logger(logger_name="api.http", file_name="parser")


class IHttp(ABC):
    @abstractmethod
    async def get(path: str, payload: dict = None) -> RetryRequestSchema:
        raise NotImplementedError


class Http(IHttp):

    def __init__(self, base_url: str) -> None:

        self.base_url = base_url
        user = fake_useragent.UserAgent().random
        self.headers = {"user-agent": user}

    # async def get(self, endpoint: str, payload: dict = None):
    #     async with aiohttp.ClientSession(
    #         base_url=self.base_url, headers=self.headers
    #     ) as session:
    #         async with session.get(
    #             url=f"{self.base_url}/{endpoint}", params=payload
    #         ) as response:
    #             print(await response.text())

    @utils.retry_request(logger=logger)
    def get(self, path: str, payload: dict = None) -> RetryRequestSchema:
        try:
            session = requests.Session()
            user = fake_useragent.UserAgent().random
            header = {"user-agent": user}
            response = session.get(
                url=f"{self.base_url}/{path}", params=payload, headers=header
            )
            # logger.info(f"{response.url}, {response.status_code}, {session.cookies}")
            return response

        except Exception as e:
            logger.error(e)
