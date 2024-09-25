from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src._utils import current_datetime
from src.modules.base.model import ModelBase


class User(ModelBase):
    """User model."""

    __tablename__ = "db_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        __type_pos=DateTime(timezone=True),
        default=current_datetime(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        __type_pos=DateTime(timezone=True),
        default=current_datetime(),
        onupdate=current_datetime(),
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return (
            f"<User id={self.id} "
            f"created_at={self.created_at} "
            f"updated_at={self.updated_at} "
            f"username={self.username} "
            f"email={self.email} >"
        )
