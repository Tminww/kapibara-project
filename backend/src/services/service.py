from typing import Annotated
from src.repositories.blocks import BlocksRepository
from src.repositories.documents import DocumentsRepository
from src.repositories.statistics import StatisticsRepository
from src.repositories.subjects import SubjectsRepository
from src.repositories.regions import RegionsRepository
from src.repositories.districts import DistrictsRepository
from src.repositories.deadlines import DeadlinesRepository
from src.repositories.organs import OrgansRepository
from src.repositories.types import DocumentTypesRepository
from src.repositories.types_in_block import TypesInBlockRepository

from src.services.blocks import BlocksService
from src.services.document import DocumentsService
from src.services.statistics import StatisticsService
from src.services.subjects import SubjectsService
from src.services.regions import RegionsService
from src.services.districts import DistrictsService
from src.services.deadlines import DeadlinesService
from src.services.organs import OrgansService
from src.services.types import DocumentTypesService
from src.services.types_in_block import TypesInBlockService


class Service:
    """This class defines a Service class with attributes for different types of services, each initialized with their respective repositories."""

    statistics: StatisticsService = StatisticsService(StatisticsRepository)
    subjects: SubjectsService = SubjectsService(SubjectsRepository)
    regions: RegionsService = RegionsService(RegionsRepository)
    districts: DistrictsService = DistrictsService(DistrictsRepository)
    deadlines: DeadlinesService = DeadlinesService(DeadlinesRepository)
    organs: OrgansService = OrgansService(OrgansRepository)
    document_types: DocumentTypesService = DocumentTypesService(DocumentTypesRepository)
    blocks: BlocksService = BlocksService(BlocksRepository)
    types_in_block: TypesInBlockService = TypesInBlockService(TypesInBlockRepository)
    documents: DocumentsService = DocumentsService(DocumentsRepository)
