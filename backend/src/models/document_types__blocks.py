from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    UniqueConstraint,
    ForeignKey,
)
from models.base import Base


class DocumentTypeBlockEntity(Base):
    __tablename__ = "document_types__blocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_doc_type: Mapped[int] = mapped_column(
        ForeignKey("document_types.id"), nullable=True
    )
    id_block: Mapped[int] = mapped_column(ForeignKey("blocks.id"), nullable=True)

    # in_deadline = relationship("DeadlineEntity", back_populates="document_types")

    __table_args__ = (
        UniqueConstraint("id", "id_doc_type", "id_block"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
