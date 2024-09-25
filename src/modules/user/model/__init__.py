import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBase


class User(ModelBase):
    """User model."""

    __tablename__ = "db_users2"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(ZoneInfo("UTC")))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(ZoneInfo("UTC")),
        onupdate=datetime.now(ZoneInfo("UTC")),
        nullable=False,
    )
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
