from .api import ApiClient
from .file import File
from .http import HttpClient
from src.config import settings

PRAVO_GOV_PATH = settings.external.EXTERNAL_PATH


class External:

    api: ApiClient = ApiClient(endpoint_name="api", http=HttpClient(base_url=PRAVO_GOV_PATH))
    file: File = File(endpoint_name="file", http=HttpClient(base_url=PRAVO_GOV_PATH))


pravo_gov = External()
