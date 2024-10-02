from typing import List

from src.repositories.types import IDocumentTypesRepository
from src.schemas.types import DocumentTypesSchema


class DocumentTypesService:
    def __init__(self, document_types_repo: IDocumentTypesRepository):
        self.document_types_repo: IDocumentTypesRepository = document_types_repo()

    async def get_all_document_types(self):
        types = await self.document_types_repo.get_all_document_types()

        return types

    async def insert_types(
        self, document_types: List[DocumentTypesSchema]
    ) -> tuple[bool, str]:

        flag, status = await self.document_types_repo.insert_or_update_document_types(
            document_types
        )

        return (flag, status)
