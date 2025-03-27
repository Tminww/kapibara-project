from .district import DistrictSchema, DistrictWithRegionsSchema
from .region import RegionSchema, RegionInfoSchema
from .act import ActSchema
from .document import DocumentSchema
from .role import RoleSchema
from .request import RequestBodySchema, RequestMaxMinBodySchema
from .response import ResponseSchema, ResponseStatSchema
from .user import (
    UserSchema,
    UserRequestSchema,
    UserInsertSchema,
    UserResponseSchema,
)

from .statistic import (
    StatAllSchema,
    StatBaseSchema,
    StatDistrictSchema,
    StatRegionSchema,
    StatPublicationSchema
)
