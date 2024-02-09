from parser.api.http import http


class Publication:

    def blocks(self):
        path = "/PublicBlocks"
        return http.get(path=path)

    def documents_on_page(self, block: str, page_size: int = 200, index: int = 1):

        path = "/Documents"
        payload = {"block": block, "PageSize": page_size, "Index": index}

        return http.get(path=path, payload=payload)

    def documents_on_page_type(
        self, npa_id: str, block: str, index: int, page_size: int = 200
    ):

        path = "/Documents"
        payload = {
            "DocumentTypes": npa_id,
            "PageSize": page_size,
            "Index": index,
            "block": block,
        }

        return http.get(path=path, payload=payload)

    def subjects(self, parent: str = "subjects"):

        path = "/PublicBlocks"
        payload = {
            "parent": parent,
        }

        return http.get(path=path, payload=payload)

    def type_all(self):

        path = "/DocumentTypes"

        return http.get(path=path)

    def type_in_subject(self, block: str):

        path = "/DocumentTypes"
        payload = {
            "block": block,
        }

        return http.get(path=path, payload=payload)


publication = Publication()
