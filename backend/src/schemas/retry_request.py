from typing import Optional
from src.schemas.base import BaseSchema


class ExternalResponseSchema(BaseSchema):
    status_code: int
    headers: dict
    content: Optional[bytes]


class RetryRequestSchema(ExternalResponseSchema):
    status: bool
    error: int
