from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint
from .base import Base


class TypeEntity(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(128))
    external_id: Mapped[str] = mapped_column(String(128))

    # documents = relationship("DocumentEntity", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("external_id", name="uq_types_external_id"),
        {"extend_existing": True},
    )
