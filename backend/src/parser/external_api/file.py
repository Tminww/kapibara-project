from .http import IHttpClient


class File:
    def __init__(self, endpoint_name: str, http: IHttpClient) -> None:
        self.http: IHttpClient = http
        self.endpoint = endpoint_name

    async def download_pdf(self, registration_number: str):
        path = f"{self.endpoint}/pdf"

        payload = {}
        if registration_number is not None:
            payload["eoNumber"] = registration_number

        response = await self.http.get(path=path, payload=payload)
        # print(*response)
        return response
