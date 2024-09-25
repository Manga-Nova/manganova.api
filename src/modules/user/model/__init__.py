from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src._utils import current_datetime
from src.modules.base.model import ModelBase


class User(ModelBase):
    """User model."""

    __tablename__ = "db_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=current_datetime())
    updated_at: Mapped[datetime] = mapped_column(
        default=current_datetime(),
        onupdate=current_datetime(),
    )
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
