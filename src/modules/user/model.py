from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBase


class User(ModelBase):
    """User model."""

    __tablename__ = "db_users"

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
