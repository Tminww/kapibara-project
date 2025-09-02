from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
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
    eo_number: Mapped[str] = mapped_column(String(32), nullable=True)
    complex_name: Mapped[str] = mapped_column(Text, nullable=True)
    pages_count: Mapped[int] = mapped_column(Integer, nullable=True)
    pdf_file_length: Mapped[int] = mapped_column(BigInteger, nullable=True)
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
    
    is_spellchek_valid: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
    
    ocr_name: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    ocr_similarity: Mapped[float] = mapped_column(nullable=True, default=None)
    
    spellcheck_errors: Mapped[str]= mapped_column(Text, nullable=True, default=None)
    
    # id_reg: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)
    # act = relationship("TypeEntity", overlaps="act", innerjoin=True)
    # region = relationship("RegionEntity", overlaps="region", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("eo_number", "id_reg", name="uq_documents_eo_number_id_reg"),
        {"extend_existing": True},
    )


Index("idx_documents_view_date", DocumentEntity.view_date)
Index("idx_documents_id_reg", DocumentEntity.id_reg)
Index("idx_documents_id_type", DocumentEntity.id_type)
