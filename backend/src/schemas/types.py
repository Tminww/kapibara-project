from typing import Optional
from pydantic import BaseModel


class PravoGovDocumentTypesSchema(BaseModel):
    name: str
    external_id: str


class DocumentTypesSchema(PravoGovDocumentTypesSchema):
    id_dl: Optional[int]
