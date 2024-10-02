from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, ForeignKey, Index
from src.models.base import Base
from src.schemas.regions import RegionDTO


class RegionEntity(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    external_id: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(10))
    parent_id: Mapped[str] = mapped_column(String(64))
    id_dist: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)

    # in_district = relationship("DistrictEntity", back_populates="regions")
    # blocks = relationship("BlockEntity", back_populates="in_region")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "external_id", "code"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )

    def to_read_model(self) -> RegionDTO:
        return RegionDTO(
            id=self.id,
            name=self.name,
            short_name=self.short_name,
            external_id=self.external_id,
            code=self.code,
            parent_id=self.parent_id,
            id_dist=self.id_dist,
        )


Index("idx_regions_external_id", RegionEntity.external_id, unique=True)
