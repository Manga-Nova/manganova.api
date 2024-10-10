from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src._utils import current_datetime
from src.modules.base.table import BaseTable
from src.settings import Settings

if TYPE_CHECKING:
    from src.modules.group.table import GroupTable


class UserTable(BaseTable):
    """UserTable model."""

    __tablename__ = "db_users"

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

    username: Mapped[str] = mapped_column(
        __type_pos=String(Settings.USERNAME_MAX_LENGTH),
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        __type_pos=String(Settings.EMAIL_MAX_LENGTH),
        unique=True,
    )
    password: Mapped[str]

    group: Mapped["GroupTable | None"] = relationship(
        "GroupTable",
        back_populates="owner",
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"< UserTable id={self.id} username={self.username} email={self.email} >"
