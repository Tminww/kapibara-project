import requests
import parser.utils.utils as utils


logger = utils.get_logger("api.http")


class Http:
    BASE_URL = "http://publication.pravo.gov.ru"

    @utils.retry(logger=logger, exception_to_check=ValueError)
    def get(self, path: str, payload: dict = None):
        try:
            response = requests.get(url=f"{self.BASE_URL}{path}", params=payload)
            print(response.url)
            return response

        except Exception as e:
            logger.error(e)


http = Http()
