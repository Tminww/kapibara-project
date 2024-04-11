from pydantic import BaseModel


class DeadlinesSchema(BaseModel):
    id: int
    day: int
