from parser.database.initiate.create import InitiateCreate
from parser.database.initiate.insert import InitiateInsert
from parser.database.initiate.update import InitiateUpdate


class Initiate:

    create = None
    insert = None
    update = None

    def __init__(
        self,
        create_interface: InitiateCreate,
        insert_interface: InitiateInsert,
        update_interface: InitiateUpdate,
    ) -> None:

        self.create = create_interface
        self.insert = insert_interface
        self.update = update_interface
