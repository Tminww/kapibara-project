from parser.api.http import http


class Publication:

    def blocks(self) -> any:
        """Обращение к апи сайта

        Returns:
            any: возвращает либо json, либо ничего. Нужно делать проверку на None
        """
        return http.get("/api/PublicBlocks/?Categories")

    def documents_on_page(self, block: str) -> any:
        """Получение документов для первой страницы заданного блока

        Args:
            code (_type_): название блока

        Returns:
            str: возвращает api по которому будет идти обращение
        """
        return http.get(f"/api/Documents?block={block}&PageSize=200&Index=1")

    def documents_on_page_type(self, npa_id: str, block: str, index: str) -> any:
        return http.get(
            f"/api/Documents?DocumentTypes={npa_id}&block={block}&PageSize=200&Index={index}"
        )

    def subjects(self) -> any:
        return http.get(f"/api/PublicBlocks/?parent=subjects")

    def type_all(self) -> any:
        return http.get(f"/api/DocumentTypes")

    def type_in_subject(self, block: str) -> any:
        return http.get(f"/api/DocumentTypes?block={block}")


publication = Publication()
