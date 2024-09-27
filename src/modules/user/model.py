from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBaseTable
from src.settings import Settings


class UserTable(ModelBaseTable):
    """UserTable model."""

    __tablename__ = "db_users"

    username: Mapped[str] = mapped_column(
        __type_pos=String(Settings.USERNAME_MAX_LENGTH),
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        __type_pos=String(Settings.EMAIL_MAX_LENGTH),
        unique=True,
    )
    password: Mapped[str]

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"< UserTable id={self.id} username={self.username} email={self.email} >"
