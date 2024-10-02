from typing import List, Optional
from src.schemas.base import BaseSchema
from src.schemas.blocks import BlockSchema


class PravoGovDocumentTypesSchema(BaseSchema):
    id: int | None
    name: str
    external_id: str


class DocumentTypesSchema(PravoGovDocumentTypesSchema):
    id_dl: Optional[int]


class TypesInBlockSchema(BaseSchema):
    id: int | None
    block: BlockSchema
    type: PravoGovDocumentTypesSchema
