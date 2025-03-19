from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Date,
    Integer,
    String,
    Text,
    UniqueConstraint,
    BigInteger,
    ForeignKey,
    Index,
    DateTime,
)
from .base import Base


class DocumentEntity(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    eo_number: Mapped[str] = mapped_column(String(16), nullable=True)
    complex_name: Mapped[str] = mapped_column(Text, nullable=True)
    pages_count: Mapped[int] = mapped_column(Integer, nullable=True)
    pdf_file_length: Mapped[int] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    document_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    signatory_authority_id: Mapped[str] = mapped_column(String(256), nullable=True)
    number: Mapped[str] = mapped_column(String(256), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    view_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    external_id: Mapped[str] = mapped_column(String(256), nullable=True)

    id_type: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=False)
    id_reg: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=False)
    hash: Mapped[str] = mapped_column(String(256), nullable=True)
    date_of_publication: Mapped[datetime] = mapped_column(Date, nullable=True)
    date_of_signing: Mapped[datetime] = mapped_column(Date, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(Date, nullable=True)

    # id_reg: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)
    # act = relationship("ActEntity", overlaps="act", innerjoin=True)
    # region = relationship("RegionEntity", overlaps="region", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("eo_number", name="uq_documents_eo_number"),
        {"extend_existing": True},
    )
