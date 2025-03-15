from .base import BaseSchema


class ActSchema(BaseSchema):
    id_act: int
    name: str
    npa_id: str
