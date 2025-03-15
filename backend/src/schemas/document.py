from datetime import date

from pydantic import ConfigDict
from .base import BaseSchema


class DocumentSchema(BaseSchema):
    id_doc: int
    id_act: int
    complexName: str
    eoNumber: int
    viewDate: date
    pagesCount: int
    id_reg: int
