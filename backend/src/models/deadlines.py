from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    UniqueConstraint,
)
from models.base import Base


class DeadlineEntity(Base):
    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[int]

    # document_types = relationship("DocumentTypeEntity", back_populates="in_deadline")

    __table_args__ = (
        UniqueConstraint("id", "day"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
