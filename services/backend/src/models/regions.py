from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, ForeignKey, Index
from models.base import Base


class RegionEntity(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(16))
    external_id: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(10))
    parent_id: Mapped[str] = mapped_column(String(64))
    id_dist: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)

    in_district = relationship("DistrictEntity", back_populates="regions")
    blocks = relationship("DistrictEntity", back_populates="in_region")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "external_id", "code"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


Index("idx_external_id", RegionEntity.external_id, unique=True)
