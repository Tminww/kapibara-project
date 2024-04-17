from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Index,
    String,
    UniqueConstraint,
)
from models.base import Base


class OrganEntity(Base):
    __tablename__ = "organs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    external_id: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(64))
    parent_id: Mapped[str] = mapped_column(String(64), nullable=True)

    blocks = relationship("BlockEntity", back_populates="in_organ")

    __table_args__ = (
        UniqueConstraint("id", "name", "external_id", "code"),
        {"extend_existing": True},
        # Index("indx_external_id", external_id),
        # Comment("Комментарий к таблице пользователей"),
    )


Index("idx_external_id", OrganEntity.external_id, unique=True)
