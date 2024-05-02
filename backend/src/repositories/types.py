from abc import ABC, abstractmethod
from typing import Annotated, List
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.errors import ResultIsEmptyError
from src.models.types import TypeEntity
from src.schemas.types import DocumentTypesSchema
from src.database.setup import async_session_maker


class IDocumentTypesRepository(ABC):
    @abstractmethod
    async def get_all_document_types() -> List[DocumentTypesSchema]:
        raise NotImplementedError

    @abstractmethod
    async def insert_or_update_document_types(
        document_types: List[DocumentTypesSchema],
    ) -> tuple[bool, str]:
        raise NotImplementedError


class DocumentTypesRepository(IDocumentTypesRepository):
    document_types = TypeEntity

    async def get_all_document_types(self) -> List[DocumentTypesSchema]:

        async with async_session_maker() as session:
            stmt = select(self.document_types)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def insert_or_update_document_types(
        self, document_types: List[DocumentTypesSchema]
    ) -> tuple[bool, str]:

        values: List[dict] = []

        for type in document_types:
            values.append(type.model_dump())

        async with async_session_maker() as session:
            stmt_insert = insert(self.document_types).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["external_id"],
                set_=dict(
                    name=stmt_insert.excluded.name,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                return (False, f"Error: {ex}")
