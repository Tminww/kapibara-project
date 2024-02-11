from parser.outgoing_requests.api import api
from parser.outgoing_requests.file import file


class Request:
    api = api
    file = file


request = Request()
