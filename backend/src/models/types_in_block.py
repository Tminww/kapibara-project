from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    UniqueConstraint,
    ForeignKey,
)
from src.models.base import Base


class TypesInBlockEntity(Base):
    __tablename__ = "types_in_block"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_block: Mapped[int] = mapped_column(ForeignKey("blocks.id"), nullable=True)
    id_type: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=True)

    # in_deadline = relationship("DeadlineEntity", back_populates="document_types")

    __table_args__ = (
        UniqueConstraint("id", "id_type", "id_block"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
