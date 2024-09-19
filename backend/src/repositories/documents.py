from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated, List
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func

from src.errors import ResultIsEmptyError
from src.models.documents import DocumentEntity
from src.schemas.documents import DocumentSchema
from src.database.setup import async_session_maker
from src.utils.utils import check_time, parser_logger

PSQL_QUERY_ALLOWED_MAX_ARGS = 32767

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


    async def insert_or_update_documents(
        self, documents: List[dict], block_type_id: int
    ) -> tuple[bool, str]:

        async with async_session_maker() as session:
            try:
                values: List[dict] = []
                for document in documents:

                    document_date = None
                    view_date = None

                    try:
                        document_date = datetime.strptime(
                            document["documentDate"], "%Y-%m-%dT%H:%M:%S"
                        ).date()
                    except Exception:
                        pass

                    try:
                        view_date = datetime.strptime(
                            document["viewDate"], "%d.%m.%Y"
                        ).date()
                    except Exception:
                        pass

                    values.append(
                        {
                            "eo_number": document.get("eoNumber", None),
                            "complex_name": document.get("complexName", None),
                            "pages_count": document.get("pagesCount", None),
                            "pdf_file_length": document.get("pdfFileLength", None),
                            "name": document.get("name", None),
                            "document_date": document_date if document_date else None,
                            "signatory_authority_id": document.get(
                                "signatoryAuthorityId", None
                            ),
                            "document_type_id": document.get("documentTypeId", None),
                            "title": document.get("title", None),
                            "view_date": view_date if view_date else None,
                            "external_id": document.get("id", None),
                            "hash": None,
                            "date_of_publication": None,
                            "date_of_signing": None,
                            "id_doc_type_block": int(block_type_id),
                        }
                    )
                
                value_object_size: int = len(values[0])
                value_objects_count: int = PSQL_QUERY_ALLOWED_MAX_ARGS // value_object_size
             
          
                values_for_insert = [values[i : i + value_objects_count] for i in range(0, len(values), value_objects_count)]

            
                for value_chunk in values_for_insert:
                    print("chunk", len(value_chunk))
          
                    stmt_insert = insert(self.documents).values(value_chunk)

                    stmt_on_conflict = stmt_insert.on_conflict_do_update(
                        index_elements=["eo_number"],
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
                    res = await session.execute(stmt_on_conflict)
                    print('inserted', res.rowcount)
                await session.commit()
                return (True, "Success")
                        
            except Exception as ex:
                parser_logger.error(f"Error occurred: {ex}")
                await session.rollback()
                return (False, f"Error: {ex}")
