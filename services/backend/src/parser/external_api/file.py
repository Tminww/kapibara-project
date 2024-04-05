from parser.external_api.http import http


class File:
    URL = "/file"

    def download_pdf(self, registration_number: str):
        path = f"{self.URL}/pdf"
        payload = {
            "eoNumber": registration_number,
        }
        response = http.get(path=path, payload=payload)
        # print(*response)
        return http.get(path=path, payload=payload)
