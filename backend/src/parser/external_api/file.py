from src.parser.external_api.http import IHttp


class File:
    def __init__(self, endpoint_name: str, http: IHttp) -> None:
        self.http: IHttp = http
        self.endpoint = endpoint_name

    def download_pdf(self, registration_number: str):
        path = f"{self.endpoint}/pdf"

        payload = {}
        if registration_number is not None:
            payload["eoNumber"] = registration_number

        response = self.http.get(path=path, payload=payload)
        # print(*response)
        return response
