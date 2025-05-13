from .subjects import router as router_subjects
from .statistics import router as router_statistics
from .dashboard import router as router_dashboard
from .parser import router as router_parser
from .validator import router as router_validator

routers = [
    router_parser,
    router_validator,
    router_subjects,
    router_statistics,
    router_dashboard,
]
