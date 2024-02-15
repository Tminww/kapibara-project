from parser.database.initiate.create import InitiateCreateInterface
from parser.database.initiate.insert import InitiateInsertInterface


class InitiateInterface(InitiateCreateInterface, InitiateInsertInterface):
    create: InitiateCreateInterface
    insert: InitiateInsertInterface


class Initiate:

    create = None
    insert = None

    def __init__(
        self,
        create_interface: InitiateCreateInterface,
        insert_interface: InitiateInsertInterface,
    ) -> None:

        self.create = create_interface
        self.insert = insert_interface
