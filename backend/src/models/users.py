from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Date,
    String,
    UniqueConstraint,
    ForeignKey,
)
from src.models.base import Base


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    hash_password: Mapped[str] = mapped_column(String(256))
    date_registered: Mapped[datetime] = mapped_column(Date)
    last_login: Mapped[datetime] = mapped_column(Date)
    is_active: Mapped[bool]

    in_role = relationship("RoleEntity", back_populates="users")

    __table_args__ = (
        UniqueConstraint("id", "username"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
