from .base import BaseSchema


class ActSchema(BaseSchema):
    id_type: int
    name: str
    npa_id: str
