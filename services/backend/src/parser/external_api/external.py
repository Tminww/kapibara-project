from parser.external_api.api import Api
from parser.external_api.file import File
from parser.external_api.http import Http
from config import settings

PRAVO_GOV_PATH = settings.external.EXTERNAL_PATH


class External:

    api: Api = Api(endpoint_name="api", http=Http(base_url=PRAVO_GOV_PATH))
    file: File = File(endpoint_name="file", http=Http(base_url=PRAVO_GOV_PATH))


pravo_gov = External()
