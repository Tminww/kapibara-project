from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    UniqueConstraint,
)
from .base import Base


class RoleEntity(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    users = relationship("UserEntity", back_populates="in_role")

    __table_args__ = (
        UniqueConstraint("id", "name"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
