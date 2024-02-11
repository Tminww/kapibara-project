from parser.outgoing_requests.http import http


class File:
    BASE_URL = "http://publication.pravo.gov.ru/file"

    def download_pdf(self, registration_number: str):
        path = f"{self.BASE_URL}/pdf"
        payload = {
            "eoNumber": registration_number,
        }
        response = http.get(path=path, payload=payload)
        # print(*response)
        return http.get(path=path, payload=payload)


file = File()
