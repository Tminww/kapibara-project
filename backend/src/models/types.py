from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Index,
    String,
    UniqueConstraint,
    ForeignKey,
)
from src.models.base import Base


class TypeEntity(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    external_id: Mapped[str] = mapped_column(String(64))
    id_dl: Mapped[int] = mapped_column(ForeignKey("deadlines.id"), nullable=True)

    # in_deadline = relationship("DeadlineEntity", back_populates="document_types")

    __table_args__ = (
        UniqueConstraint("id", "name", "external_id"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


Index("idx_types_external_id", TypeEntity.external_id, unique=True)
