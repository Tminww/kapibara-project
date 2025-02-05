from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, String, BigInteger, UniqueConstraint, Text
from database.setup import Base

class DocumentEntity(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    complex_name: Mapped[str] = mapped_column(Text)
    id_act: Mapped[int] = mapped_column(ForeignKey("act.id"), nullable=False)
    eo_number: Mapped[str] = mapped_column(String(16))
    view_date: Mapped[datetime] = mapped_column(Date)
    pages_count: Mapped[int]
    id_reg: Mapped[int] = mapped_column(ForeignKey("region.id"), nullable=False)
    # act = relationship("ActEntity", overlaps="act", innerjoin=True)
    # region = relationship("RegionEntity", overlaps="region", innerjoin=True)

    __table_args__ = (
        UniqueConstraint("id", "complex_name", "eo_number"),
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

    
