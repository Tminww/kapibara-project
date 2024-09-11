from abc import ABC, abstractmethod
from typing import Annotated, List
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

from src.errors import ResultIsEmptyError
from src.models.documents import DocumentEntity
from src.schemas.documents import DocumentSchema
from src.database.setup import async_session_maker


class IDocumentsRepository(ABC):
    @abstractmethod
    async def get_all_documents() -> List[DocumentSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_document(id_item: int) -> List[DocumentSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_documents_count_in_block(block_type_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_documents(
        documents: List[DocumentSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError


class DocumentsRepository(IDocumentsRepository):
    documents = DocumentEntity

    async def get_documents_count_in_block(self, block_type_id: int) -> int:
        async with async_session_maker() as session:
            stmt = select(func.count(self.documents.id)).where(
                self.documents.id_doc_type_block == block_type_id
            )
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_all_documents(self) -> List[DocumentSchema]:

        async with async_session_maker() as session:
            stmt = select(self.documents)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_document(self, item_id: int) -> List[DocumentSchema]:

        async with async_session_maker() as session:
            stmt = select(self.documents).where(self.documents.id == item_id)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_documents(
        self, documents: List[DocumentSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for document in documents:
            values.append(document.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.documents).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    name=stmt_insert.excluded.name,
                    short_name=stmt_insert.excluded.short_name,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")
