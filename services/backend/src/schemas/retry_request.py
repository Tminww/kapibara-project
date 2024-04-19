from pydantic import BaseModel
from requests import Response
import requests


class RetryRequestSchema(BaseModel):
    status: bool
    headers: dict
    content: bytes
    error: int
