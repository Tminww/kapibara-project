from typing import List
from .base import BaseSchema


class SubjectBaseSchema(BaseSchema):
    id: int
    name: str


class SubjectWithRegionsSchema(SubjectBaseSchema):
    regions: List[SubjectBaseSchema]
