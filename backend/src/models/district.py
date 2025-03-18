from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint
from .base import Base

#   CREATE TABLE IF NOT EXISTS district (
#     id INT PRIMARY KEY,
#     name VARCHAR(64),
#     UNIQUE (id, name),
#     )


class DistrictEntity(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    short_name: Mapped[str] = mapped_column(String(64))

    __table_args__ = (
        UniqueConstraint("id", "name", name="uq_districts_id_name"),
        {"extend_existing": True},
    )
