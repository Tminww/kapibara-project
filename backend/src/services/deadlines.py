from typing import List
from repositories.deadlines import IDeadlinesRepository
from schemas.deadlines import DeadlinesSchema


class DeadlinesService:
    def __init__(self, deadlines_repo: IDeadlinesRepository):
        self.deadlines_repo: IDeadlinesRepository = deadlines_repo()

    async def get_all_deadlines(self):
        deadlines = await self.deadlines_repo.get_all_deadlines()

        return deadlines

    async def get_deadline_by_id(self, item_id: int):
        deadlines = await self.deadlines_repo.get_deadline(item_id)

        return deadlines

    async def insert_deadlines(
        self, deadlines: List[DeadlinesSchema]
    ) -> tuple[bool, str]:

        flag, status = await self.deadlines_repo.insert_or_update_deadlines(deadlines)

        return (flag, status)

    async def delete_deadline_by_id(self, item_id: int):
        flag, status = await self.deadlines_repo.delete_deadline(item_id)

        return (flag, status)
