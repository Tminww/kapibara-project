from api.subjects import router as router_subjects
from api.statistics import router as router_statistics
from api.regions import router as router_regions
from api.districts import router as router_districts


all_routers = [
    router_subjects,
    router_statistics,
    router_regions,
    router_districts,
]
