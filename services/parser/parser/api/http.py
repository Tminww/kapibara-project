import requests
import parser.utils.utils as utils
import fake_useragent

logger = utils.get_logger("api.http")


class Http:
    BASE_URL = "http://publication.pravo.gov.ru"

    @utils.retry_request(logger=logger, exception_to_check=ValueError)
    def get(self, path: str, payload: dict = None):
        try:
            session = requests.Session()
            user = fake_useragent.UserAgent().random()
            header = {"user-agent": user}
            response = session.get(
                url=f"{self.BASE_URL}{path}", params=payload, headers=header
            )
            print(response.url)
            return response

        except Exception as e:
            logger.error(e)


http = Http()
