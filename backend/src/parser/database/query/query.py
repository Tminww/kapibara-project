from parser.database.query.insert import QueryInsert
from parser.database.query.update import QueryUpdate
from parser.database.query.select import QuerySelect


class Query:

    insert: None
    update: None
    select: None

    def __init__(
        self,
        insert_interface: QueryInsert,
        update_interface: QueryUpdate,
        select_interface: QuerySelect,
    ) -> None:

        self.insert = insert_interface
        self.update = update_interface
        self.select = select_interface
