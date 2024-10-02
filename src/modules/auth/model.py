from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBaseTable


class OldHashTable(ModelBaseTable):
    """Old hash model."""

    __tablename__ = "db_old_hashes"

    user_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    password: Mapped[str]

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"<OldHashTable user_id={self.user_id} password={self.password} >"
