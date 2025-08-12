from schemas import RequestTableSchema
from repositories.table import TableRepository


class TableService:

    def __init__(self, repository: TableRepository):
        self.repository: TableRepository = repository()

    async def get_rows_from_table(self, params: RequestTableSchema):
        response = []
        if params.type =="year":
            
            response = await self.repository.get_rows_from_table_by_year(params=params)
        elif params.type == "region":
            response = await self.repository.get_rows_from_table_by_region(params=params)

        elif params.type =="type":
            response = await self.repository.get_rows_from_table_by_type(params=params)

        else:
            ...
            
        return response
