```
alembic init -t async alembic 

config.set_main_option("sqlalchemy.url", settings.get_db_url())

from app.models import *  # noqa: F403

target_metadata = Base.metadata


```