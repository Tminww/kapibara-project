from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    UniqueConstraint,
)
from src.models.base import Base


class DistrictEntity(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    short_name: Mapped[str] = mapped_column(String(8))

    regions = relationship("RegionEntity", back_populates="in_district")
    in_region = relationship("RegionEntity", back_populates="blocks")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
