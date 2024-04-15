from parser.external_api.api import Api
from parser.external_api.file import File
from parser.external_api.http import Http


class Request:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @property
    def api(self):
        return Api(endpoint_name="api", http=Http(base_url=self.base_url))

    @property
    def file(self):
        return File(endpoint_name="file", http=Http(base_url=self.base_url))


request = Request(base_url="http://publication.pravo.gov.ru")
