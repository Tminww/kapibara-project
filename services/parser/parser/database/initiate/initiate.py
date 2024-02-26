from parser.database.initiate.create import InitiateCreate
from parser.database.initiate.insert import InitiateInsert


class Initiate:

    create = None
    insert = None

    def __init__(
        self,
        create_interface: InitiateCreate,
        insert_interface: InitiateInsert,
    ) -> None:

        self.create = create_interface
        self.insert = insert_interface
