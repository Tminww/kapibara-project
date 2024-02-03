import requests
from parser.log.createLogger import get_logger


logger = get_logger("api.http")


class Http:
    BASE_URL = "http://publication.pravo.gov.ru"

    def get(self, path: str):
        try:
            response = requests.get(url=f"{self.BASE_URL}{path}")
            return response.json()

        except Exception as e:
            logger.error(e)


http = Http()
