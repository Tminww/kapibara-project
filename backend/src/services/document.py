from typing import List

from src.repositories.documents import IDocumentsRepository
from src.schemas.documents import DocumentSchema


class DocumentsService:
    def __init__(self, documents_repo: IDocumentsRepository):
        self.documents_repo: IDocumentsRepository = documents_repo()

    async def get_all_documents(self):
        documents = await self.documents_repo.get_all_documents()

        return documents
    async def get_documents_count_in_block(self, block_type_id) -> int:
        count = await self.documents_repo.get_documents_count_in_block(block_type_id)

        return count

    async def get_document_by_id(self, item_id: int):
        documents = await self.documents_repo.get_document(item_id)

        return documents

    async def insert_documents(
        self, documents: List[DocumentSchema]
    ) -> tuple[bool, str]:

        flag, status = await self.documents_repo.insert_or_update_documents(documents)

        return (flag, status)
