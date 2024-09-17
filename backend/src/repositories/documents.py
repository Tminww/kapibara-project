from abc import ABC, abstractmethod
import datetime
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
        documents: List[dict],
        block_type_id: int,
    ) -> tuple[bool, str]:
        raise NotImplementedError


class DocumentsRepository(IDocumentsRepository):
    documents = DocumentEntity

    async def get_documents_count_in_block(self, block_type_id: int) -> int:
        async with async_session_maker() as session:
            stmt = (
                select(func.count())
                .select_from(self.documents)
                .where(self.documents.id_doc_type_block == block_type_id)
            )
            res = await session.execute(stmt)
            count = res.scalar()

            if count is not None:
                return count
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

    async def test_insert_or_update_documents(self):
        async with async_session_maker() as session:
            stmt_on_conflict = (
                insert(self.documents)
                .values(
                    [
                        {
                            "eo_number": "0001202210060013",
                            "complex_name": "Конституция Российской Федерации",
                            "pages_count": 76,
                            "pdf_file_length": 3871723,
                            "name": "",
                            "document_date": "2022-10-06",
                            "signatory_authority_id": "225698f1-cfbc-4e42-9caa-32f9f7403211",
                            "document_type_id": "8fb60238-9fee-4a1b-9534-6d99ad0ceff0",
                            "title": "Конституция Российской Федерации",
                            "view_date": "2022-10-06",
                            "external_id": "6eb0448a-713a-4279-bab3-0ef51c8a62ad",
                            "hash": None,
                            "date_of_publication": None,
                            "date_of_signing": None,
                            "id_doc_type_block": 1,
                        },
                        # Добавьте другие записи
                    ]
                )
                .on_conflict_do_update(
                    index_elements=["id"],
                    set_={
                        "eo_number": "excluded.eo_number",
                        "complex_name": "excluded.complex_name",
                        "pages_count": "excluded.pages_count",
                        "pdf_file_length": "excluded.pdf_file_length",
                        "name": "excluded.name",
                        "document_date": "excluded.document_date",
                        "signatory_authority_id": "excluded.signatory_authority_id",
                        "document_type_id": "excluded.document_type_id",
                        "title": "excluded.title",
                        "view_date": "excluded.view_date",
                        "external_id": "excluded.external_id",
                        "hash": "excluded.hash",
                        "date_of_publication": "excluded.date_of_publication",
                        "date_of_signing": "excluded.date_of_signing",
                        "id_doc_type_block": "excluded.id_doc_type_block",
                    },
                )
            )
            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                print(f"Error occurred: {ex}")
                await session.rollback()
                return (False, f"Error: {ex}")

    async def insert_or_update_documents(
        self, documents: List[dict], block_type_id: int
    ) -> tuple[bool, str]:
        print("insert_or_update_documents")
        values: List[dict] = []

        for document in documents:
            document_date = (
                datetime.strptime(document["documentDate"], "%Y-%m-%d").date()
                if document["documentDate"]
                else None
            )
            view_date = (
                datetime.strptime(document["viewDate"], "%Y-%m-%d").date()
                if document["viewDate"]
                else None
            )
            values.append(
                {
                    "eo_number": document["eoNumber"],
                    "complex_name": document["complexName"],
                    "pages_count": document["pagesCount"],
                    "pdf_file_length": document["pdfFileLength"],
                    "name": document["name"],
                    "document_date": document_date,
                    "signatory_authority_id": document["signatoryAuthorityId"],
                    "document_type_id": document["documentTypeId"],
                    "title": document["title"],
                    "view_date": view_date,
                    "external_id": document["id"],
                    "hash": None,
                    "date_of_publication": None,
                    "date_of_signing": None,
                    "id_doc_type_block": block_type_id,
                }
            )

        async with async_session_maker() as session:
            stmt_insert = insert(self.documents).values(values)

            stmt_on_conflict = stmt_insert.on_conflict_do_update(
                index_elements=["id"],
                set_=dict(
                    eo_number=stmt_insert.excluded.eo_number,
                    complex_name=stmt_insert.excluded.complex_name,
                    pages_count=stmt_insert.excluded.pages_count,
                    pdf_file_length=stmt_insert.excluded.pdf_file_length,
                    name=stmt_insert.excluded.name,
                    document_date=stmt_insert.excluded.document_date,
                    signatory_authority_id=stmt_insert.excluded.signatory_authority_id,
                    document_type_id=stmt_insert.excluded.document_type_id,
                    title=stmt_insert.excluded.title,
                    view_date=stmt_insert.excluded.view_date,
                    external_id=stmt_insert.excluded.external_id,
                    hash=stmt_insert.excluded.hash,
                    date_of_publication=stmt_insert.excluded.date_of_publication,
                    date_of_signing=stmt_insert.excluded.date_of_signing,
                    id_doc_type_block=stmt_insert.excluded.id_doc_type_block,
                ),
            )

            try:
                res = await session.execute(stmt_on_conflict)
                await session.commit()
                return (True, "Success")
            except Exception as ex:
                print(f"Error occurred: {ex}")
                await session.rollback()
                return (False, f"Error: {ex}")
