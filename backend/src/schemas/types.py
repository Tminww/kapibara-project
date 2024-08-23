from typing import Optional
from src.schemas.base import BaseSchema


class PravoGovDocumentTypesSchema(BaseSchema):
    id: int | None
    name: str
    external_id: str


class DocumentTypesSchema(PravoGovDocumentTypesSchema):
    id_dl: Optional[int]
