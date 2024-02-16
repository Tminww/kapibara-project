from parser.database.query.insert import QueryInsertInterface
from parser.database.query.update import QueryUpdateInterface
from parser.database.query.select import QuerySelectInterface


class QueryInterface(QueryInsertInterface, QueryUpdateInterface, QuerySelectInterface):
    insert: QueryInsertInterface
    update: QueryUpdateInterface
    select: QuerySelectInterface


class Query:

    insert: None
    update: None
    select: None

    def __init__(
        self,
        insert_interface: QueryInsertInterface,
        update_interface: QueryUpdateInterface,
        select_interface: QuerySelectInterface,
    ) -> None:

        self.insert = insert_interface
        self.update = update_interface
        self.select = select_interface
