from parser.database.setup import get_sync_connection

from parser.database.initiate.initiate import InitiateInterface, Initiate
from parser.database.initiate.create import InitiateCreate
from parser.database.initiate.insert import InitiateInsert
from parser.database.query.query import QueryInterface, Query
from parser.database.query.insert import QueryInsert
from parser.database.query.update import QueryUpdate
from parser.database.query.select import QuerySelect

connection = get_sync_connection


class Database:

    initiate = None
    query = None

    def __init__(
        self, initiate_interface: InitiateInterface, query_interface: QueryInterface
    ) -> None:

        self.initiate = initiate_interface
        self.query = query_interface


db = Database(
    Initiate(InitiateCreate(connection), InitiateInsert(connection)),
    Query(QueryInsert(connection), QueryUpdate(connection), QuerySelect(connection)),
)
