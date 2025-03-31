from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, ForeignKey, Index
from .base import Base


class RegionEntity(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    external_id: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(32))
    id_dist: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)

    # in_district = relationship("DistrictEntity", back_populates="regions")
    # blocks = relationship("BlockEntity", back_populates="in_region")

    __table_args__ = (
        UniqueConstraint(
            "external_id", name="uq_regions_external_id"
        ),  # Уникальное ограничение для ON CONFLICT
        {"extend_existing": True},
    )


# Если нужен уникальный индекс на code отдельно, можно добавить:
# Index("idx_regions_code_unique", RegionEntity.code, unique=True)
Index("idx_regions_id_dist", RegionEntity.id_dist)
