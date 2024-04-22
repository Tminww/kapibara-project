from parser.external_api.http import Http, IHttp
from schemas.retry_request import RetryRequestSchema


class Api:

    def __init__(self, endpoint_name: str, http: IHttp) -> None:
        self.http: IHttp = http
        self.endpoint = endpoint_name

    def documents_for_the_block(
        self, block: str, index: int, page_size: int = 200, document_type: str = None
    ) -> RetryRequestSchema:
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

        path = f"{self.endpoint}/Documents"
        payload = {
            "PageSize": page_size,
            "Index": index,
            "block": block,
        }
        if document_type is not None:
            payload["DocumentTypes"] = document_type

        return self.http.get(path=path, payload=payload)

    def public_blocks(self, parent: str = None) -> RetryRequestSchema:

        path = f"{self.endpoint}/PublicBlocks"
        payload = {}
        if parent is not None:
            payload["parent"] = parent

        return self.http.get(path=path, payload=payload)

    def types_in_block(self, block: str = None) -> RetryRequestSchema:
        """Получение номенклатуры для конкретного блока

        Args:
            block (str, optional): указывается блок.
            По умолчанию выводит номенклатуру для всех блоков. Defaults to None.

        Returns:
            json: ответ сервера
        """

        path = f"{self.endpoint}/DocumentTypes"

        payload = {}
        if block is not None:
            payload["block"] = block

        return self.http.get(path=path, payload=payload)
