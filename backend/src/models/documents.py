from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Date,
    String,
    Text,
    UniqueConstraint,
    BigInteger,
    ForeignKey,
)
from src.models.base import Base


class DocumentEntity(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    eo_number: Mapped[str] = mapped_column(String(16))
    hash: Mapped[str] = mapped_column(String(256), nullable=True)
    pages_count: Mapped[int]
    date_of_publication: Mapped[datetime] = mapped_column(Date)
    date_of_signing: Mapped[datetime] = mapped_column(Date)
    id_doc_type_block: Mapped[int] = mapped_column(ForeignKey("types_in_block.id"))
    # id_reg: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)
    # act = relationship("ActEntity", overlaps="act", innerjoin=True)
    # region = relationship("RegionEntity", overlaps="region", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("id", "name", "eo_number"),
        {"extend_existing": True},
    )

    # def to_read_model(self) -> DocumentSchema:
    #     return DocumentSchema(
    #         id_doc=self.id,
    #         complexName=self.complex_name,
    #         id_act=self.id_act,
    #         eoNumber=self.eo_number,
    #         viewDate=self.view_date,
    #         pagesCount=self.pages_count,
    #         id_reg=self.id_reg,
    #     )
