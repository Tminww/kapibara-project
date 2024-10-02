from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    UniqueConstraint,
    ForeignKey,
)
from src.models.base import Base


class BlockEntity(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(primary_key=True)

    id_organ: Mapped[int] = mapped_column(ForeignKey("organs.id"), nullable=True)
    id_reg: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)

    in_organ = relationship("OrganEntity", back_populates="blocks")
    in_region = relationship("RegionEntity", back_populates="blocks")

    __table_args__ = (
        UniqueConstraint("id", "id_organ", "id_reg"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
