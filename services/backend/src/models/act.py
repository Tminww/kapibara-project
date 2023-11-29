from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint
from database.setup import Base

class ActEntity(Base):
    __tablename__ = "act"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    npa_id: Mapped[str] = mapped_column(String(128))

    # documents = relationship("DocumentEntity", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("name", "npa_id"),
        {"extend_existing": True},
    )


