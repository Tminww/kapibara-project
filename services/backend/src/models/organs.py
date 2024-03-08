from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    UniqueConstraint,
)
from models.base import Base


class OrganEntity(Base):
    __tablename__ = "organs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(64))

    blocks = relationship("BlockEntity", back_populates="in_organ")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "code"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
