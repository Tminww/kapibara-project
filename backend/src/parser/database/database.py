from database.setup import get_async_session

from parser.database.initiate.initiate import Initiate
from parser.database.initiate.create import InitiateCreate
from parser.database.initiate.insert import InitiateInsert
from parser.database.initiate.update import InitiateUpdate

from parser.database.query.query import Query
from parser.database.query.insert import QueryInsert
from parser.database.query.update import QueryUpdate
from parser.database.query.select import QuerySelect

connection = get_async_session


class Database:

    initiate = None
    query = None

    def __init__(self, initiate_interface: Initiate, query_interface: Query) -> None:

        self.initiate = initiate_interface
        self.query = query_interface


db = Database(
    Initiate(
        InitiateCreate(connection),
        InitiateInsert(connection),
        InitiateUpdate(connection),
    ),
    Query(
        QueryInsert(connection),
        QueryUpdate(connection),
        QuerySelect(connection),
    ),
)
