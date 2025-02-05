from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint, ForeignKey
from database.setup import Base


class RegionEntity(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_dist: Mapped[int] = mapped_column(ForeignKey("district.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(128))
    code: Mapped[str] = mapped_column(String(16))

    # documents = relationship("DocumentEntity", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("name", "code"),
        {"extend_existing": True},
    )
