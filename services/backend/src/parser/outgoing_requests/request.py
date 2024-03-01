from parser.outgoing_requests.api import Api
from parser.outgoing_requests.file import File


class Request:
    api = Api()
    file = File()


request = Request()
