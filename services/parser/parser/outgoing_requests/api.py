from parser.outgoing_requests.http import http


class Api:
    BASE_URL = "http://publication.pravo.gov.ru/api"

    def all_blocks(self):
        path = f"{self.BASE_URL}/PublicBlocks"
        return http.get(path=path)

    def documents_for_the_block(
        self, block: str, index: int, page_size: int = 200, document_type: str = None
    ):
        """Выводит документы для указанного блока с соответствующим типом.
           Если тип не указан - выводит для всего блока.

        Args:
            block (str): код блока
            index (int): страница
            page_size (int, optional): Количество документов на странице. Defaults to 200.
            document_type (str, optional): Тип документа. Defaults to None.

        Returns:
            json: ответ сервера
        """

        path = f"{self.BASE_URL}/Documents"
        payload = {
            "DocumentTypes": document_type,
            "PageSize": page_size,
            "Index": index,
            "block": block,
        }

        return http.get(path=path, payload=payload)

    def subblocks(self, parent: str = "subjects"):

        path = f"{self.BASE_URL}/PublicBlocks"
        payload = {
            "parent": parent,
        }

        return http.get(path=path, payload=payload)

    def types_in_block(self, block: str = None):
        """Получение номенклатуры для конкретного блока

        Args:
            block (str, optional): указывается блок.
            По умолчанию выводит номенклатуру для всех блоков. Defaults to None.

        Returns:
            json: ответ сервера
        """

        path = f"{self.BASE_URL}/DocumentTypes"
        payload = {
            "block": block,
        }

        return http.get(path=path, payload=payload)


api = Api()
