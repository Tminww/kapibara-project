from parser.database.setup import get_sync_connection
from parser.database.initiate import Initiate


class Database:

    initiate = Initiate(get_connection=get_sync_connection)
    query = None


db = Database()
