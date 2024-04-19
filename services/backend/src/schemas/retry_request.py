from typing import Optional
from pydantic import BaseModel


class RetryRequestSchema(BaseModel):
    status: bool
    headers: dict
    content: Optional[bytes]
    error: int
