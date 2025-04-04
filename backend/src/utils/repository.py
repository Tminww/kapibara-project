from abc import ABC, abstractmethod
from datetime import datetime


from src.models.documents import DocumentEntity
from src.models.regions import RegionEntity
from src.models.districts import DistrictEntity

from src.schemas.subjects import SubjectInfoDTO
from src.schemas.statistics import StatRowSchema, StatBaseDTO, RequestBodySchema

from sqlalchemy import insert, select, func

from src.database.setup import async_session_maker
from src.errors import ResultIsEmptyError


class AbstractRepository(ABC):
    @abstractmethod
    async def get_stat_in_region(parameters, id_reg):
        raise NotImplementedError

    @abstractmethod
    async def get_districts():
        raise NotImplementedError

    @abstractmethod
    async def get_regions_in_district(id_dist):
        raise NotImplementedError

    @abstractmethod
    async def get_definite_regions_in_district(parameters, id_dist):
        raise NotImplementedError

    @abstractmethod
    async def get_districts_by_regions(regions):
        raise NotImplementedError

    @abstractmethod
    async def get_stat_in_district(parameters, id_dist):
        raise NotImplementedError

    @abstractmethod
    async def get_stat_all(parameters):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    document: DocumentEntity = None
    region: RegionEntity = None
    # act: ActEntity = None
    district: DistrictEntity = None

    async def get_definite_regions_in_district(
        self, parameters: RequestBodySchema, id_dist
    ):
        async with async_session_maker() as session:
            stmt = select(self.region).filter(
                (parameters.regions is None or self.region.id.in_(parameters.regions)),
                (self.region.id_dist == id_dist),
            )
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_all(self, parameters: RequestBodySchema):
        async with async_session_maker() as session:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_date = datetime.strptime(current_date, "%Y-%m-%d")

            if parameters.start_date is None and parameters.end_date is None:
                start_date = None
                end_date = None
            elif parameters.start_date is None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
            elif parameters.start_date is not None and parameters.end_date is None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = current_date
            elif parameters.start_date is not None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
            print(type(start_date), end_date, sep=" ")
            stmt = (
                select(
                    self.act.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(self.document)
                .join(self.region, self.document.id_reg == self.region.id)
                .join(self.act, self.document.id_act == self.act.id)
                .filter(
                    (
                        parameters.regions is None
                        or self.region.id.in_(parameters.regions)
                    ),
                    (
                        parameters.start_date is None
                        and parameters.end_date is None
                        or self.document.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(self.act.name)
                .order_by(self.act.name)
            )
            res = await session.execute(stmt)
            print(res)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]
            print(res)
            if res:
                return res
            else:
                print("get_stat_all")
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_in_district(self, parameters: RequestBodySchema, id_dist):
        async with async_session_maker() as session:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_date = datetime.strptime(current_date, "%Y-%m-%d")

            if parameters.start_date is None and parameters.end_date is None:
                start_date = None
                end_date = None
            elif parameters.start_date is None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
            elif parameters.start_date is not None and parameters.end_date is None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = current_date
            elif parameters.start_date is not None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")

            stmt = (
                select(
                    self.act.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(self.document)
                .join(self.region, self.document.id_reg == self.region.id)
                .join(self.act, self.document.id_act == self.act.id)
                .filter(
                    (self.region.id_dist == id_dist),
                    (
                        parameters.regions is None
                        or self.region.id.in_(parameters.regions)
                    ),
                    (
                        start_date is None
                        and end_date is None
                        or self.document.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(self.act.name)
                .order_by(self.act.name)
            )
            res = await session.execute(stmt)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]

            return res
            # if res:
            #     return res
            # else:
            #     raise ResultIsEmptyError("Result is empty")

    async def get_districts_by_regions(self, regions):
        async with async_session_maker() as session:
            stmt_for_district_id = (
                select(self.region.id_dist)
                .select_from(self.region)
                .filter(regions is None or self.region.id.in_(regions))
            )
            districts_id = await session.execute(stmt_for_district_id)

            districts_id = [row[0] for row in districts_id.all()]

            stmt = select(self.district).filter(
                regions is None or self.district.id.in_(districts_id)
            )

            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                print("get_stat_in_district")
                raise ResultIsEmptyError("Result is empty")

    async def get_districts(self):
        async with async_session_maker() as session:
            stmt = select(self.district)
            res = await session.execute(stmt)

            res = [row[0] for row in res.all()]

            if res:
                return res
            else:
                print("get_districts")
                raise ResultIsEmptyError("Result is empty")

    async def get_regions_in_district(self, id_dist):
        async with async_session_maker() as session:
            stmt = select(self.region).filter(self.region.id_dist == id_dist)
            res = await session.execute(stmt)

            res = [SubjectInfoDTO(name=row[0].name, id=row[0].id) for row in res.all()]

            if res:
                return res
            else:
                print("get_regions_in_district")
                raise ResultIsEmptyError("Result is empty")

    async def get_stat_in_region(self, parameters: RequestBodySchema, id_reg):
        async with async_session_maker() as session:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_date = datetime.strptime(current_date, "%Y-%m-%d")

            if parameters.start_date is None and parameters.end_date is None:
                start_date = None
                end_date = None
            elif parameters.start_date is None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")
            elif parameters.start_date is not None and parameters.end_date is None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = current_date
            elif parameters.start_date is not None and parameters.end_date is not None:
                start_date = datetime.strptime(parameters.start_date, "%Y-%m-%d")
                end_date = datetime.strptime(parameters.end_date, "%Y-%m-%d")

            stmt = (
                select(
                    self.act.name.label("name"),
                    func.count().label("count"),
                )
                .select_from(self.document)
                .join(self.region, self.document.id_reg == self.region.id)
                .join(self.act, self.document.id_act == self.act.id)
                .filter(
                    (self.region.id == id_reg),
                    (
                        parameters.start_date is None
                        and parameters.end_date is None
                        or self.document.view_date.between(start_date, end_date)
                    ),
                )
                .group_by(self.act.name)
                .order_by(self.act.name)
            )
            res = await session.execute(stmt)
            res = [StatBaseDTO(name=row.name, count=row.count) for row in res.all()]

            # if res:
            #     return res
            # else:
            #     raise ResultIsEmptyError("Result is empty")
            return res
