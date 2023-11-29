from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint
from database.setup import Base

    #   CREATE TABLE IF NOT EXISTS district (
    #     id INT PRIMARY KEY,
    #     name VARCHAR(64),
    #     UNIQUE (id, name), 
    #     )

class DistrictEntity(Base):
    __tablename__ = "district"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    __table_args__ = (
        UniqueConstraint("id", "name"),
        {"extend_existing": True},
    )
