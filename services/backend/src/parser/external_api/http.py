import requests
from utils import utils
import fake_useragent

logger = utils.get_logger("api.http")


class Http:
    BASE_URL = "http://publication.pravo.gov.ru"

    @utils.retry_request(logger=logger)
    def get(self, path: str, payload: dict = None):
        try:
            session = requests.Session()
            user = fake_useragent.UserAgent().random
            header = {"user-agent": user}
            response = session.get(
                url=f"{self.BASE_URL}{path}", params=payload, headers=header
            )
            # logger.info(f"{response.url}, {response.status_code}, {session.cookies}")
            return response

        except Exception as e:
            logger.error(e)


http = Http()
