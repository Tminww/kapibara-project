from typing import Optional
from pydantic import BaseModel


class ExternalResponseSchema(BaseModel):
    status_code: int
    headers: dict
    content: Optional[bytes]


class RetryRequestSchema(ExternalResponseSchema):
    status: bool
    error: int
