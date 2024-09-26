from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBase


class Title(ModelBase):
    """Title model."""

    __tablename__ = "db_titles"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(__type_pos=String(2000), nullable=True)
    summary: Mapped[str] = mapped_column(__type_pos=String(500), nullable=True)

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"<Title id={self.id} name={self.name} summary={self.summary} >"
