from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src._utils import current_datetime
from src.modules.base.table import BaseTable

if TYPE_CHECKING:
    from src.modules.user.table import UserTable


class GroupTable(BaseTable):
    __tablename__ = "db_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, sort_order=-1)
    created_at: Mapped[datetime] = mapped_column(
        __type_pos=DateTime(timezone=True),
        default=current_datetime,
        sort_order=-1,
    )
    updated_at: Mapped[datetime] = mapped_column(
        __type_pos=DateTime(timezone=True),
        default=current_datetime,
        onupdate=current_datetime,
        sort_order=-1,
    )

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(
        __type_pos=String(length=2000),
        nullable=True,
        default=None,
    )

    owner_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_users.id", ondelete="CASCADE"),
        unique=True,
    )

    owner: Mapped["UserTable"] = relationship("UserTable", back_populates="group")

    members: Mapped[list["UserTable"]] = relationship(
        "UserTable",
        secondary="db_group_members",
    )

    followers: Mapped[list["UserTable"]] = relationship(
        "UserTable",
        secondary="db_group_followers",
    )


class GroupMembersTable(BaseTable):
    __tablename__ = "db_group_members"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("db_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("db_users.id", ondelete="CASCADE"),
        primary_key=True,
    )


class GroupFollowersTable(BaseTable):
    __tablename__ = "db_group_followers"

    group_id: Mapped[int] = mapped_column(
        ForeignKey("db_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("db_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
