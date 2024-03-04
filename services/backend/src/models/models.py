from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Date,
    Index,
    String,
    Text,
    UniqueConstraint,
    BigInteger,
    ForeignKey,
)
from database.setup import Base


class DistrictEntity(Base):
    __tablename__ = "districts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    short_name: Mapped[str] = mapped_column(String(8))

    regions = relationship("RegionEntity", back_populates="in_district")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class RegionEntity(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(16))
    external_id: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(10))
    parent_id: Mapped[str] = mapped_column(String(64))
    id_dist: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)

    in_district = relationship("DistrictEntity", back_populates="regions")
    blocks = relationship("DistrictEntity", back_populates="in_region")
    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "external_id", "code"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class OrganEntity(Base):
    __tablename__ = "organs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(64))

    blocks = relationship("BlockEntity", back_populates="in_organ")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "code"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class BlockEntity(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    short_name: Mapped[str] = mapped_column(String(64))
    id_organ: Mapped[int] = mapped_column(ForeignKey("organs.id"), nullable=True)
    id_reg: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)

    in_organ = relationship("OrganEntity", back_populates="blocks")
    in_region = relationship("RegionEntity", back_populates="blocks")

    __table_args__ = (
        UniqueConstraint("id", "name", "short_name", "id_organ", "id_reg"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class DeadlineEntity(Base):
    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[int]

    document_types = relationship("DocumentTypeEntity", back_populates="in_deadline")

    __table_args__ = (
        UniqueConstraint("id", "day"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class DocumentTypeEntity(Base):
    __tablename__ = "document_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    external_id: Mapped[str] = mapped_column(String(64))
    id_dl: Mapped[int] = mapped_column(ForeignKey("deadlines.id"), nullable=True)

    in_deadline = relationship("DeadlineEntity", back_populates="document_types")

    __table_args__ = (
        UniqueConstraint("id", "name", "external_id"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


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


class DocumentEntity(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    eo_number: Mapped[str] = mapped_column(String(16))
    hash: Mapped[str] = mapped_column(String(256), nullable=True)
    pages_count: Mapped[int]
    date_of_publication: Mapped[datetime] = mapped_column(Date)
    date_of_signing: Mapped[datetime] = mapped_column(Date)
    id_doc_type_block: Mapped[int] = mapped_column(
        ForeignKey("document_types__blocks.id")
    )
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


class RoleEntity(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))

    users = relationship("UserEntity", back_populates="in_role")

    __table_args__ = (
        UniqueConstraint("id", "name"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    hash_password: Mapped[str] = mapped_column(String(256))
    date_registered: Mapped[datetime] = mapped_column(Date)
    last_login: Mapped[datetime] = mapped_column(Date)
    is_active: Mapped[bool]

    in_role = relationship("RoleEntity", back_populates="users")

    __table_args__ = (
        UniqueConstraint("id", "username"),
        {"extend_existing": True},
        # Index("ix_users_role_id", role_id),
        # Comment("Комментарий к таблице пользователей"),
    )
