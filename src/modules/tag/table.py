from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modules.base.table import BaseTable
from src.modules.tag.enums import TagGroupEnum

if TYPE_CHECKING:
    from src.modules.title.table import TitleTable


class TagTable(BaseTable):
    """Tag model."""

    __tablename__ = "db_tags"

    name: Mapped[str] = mapped_column(__type_pos=String(100), unique=True)
    group: Mapped[TagGroupEnum] = mapped_column(__type_pos=String(100), index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    titles: Mapped[list["TitleTable"]] = relationship(
        "TitleTable",
        secondary="db_title_tags",
        back_populates="tags",
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"< Tag id={self.id} name={self.name} group={self.group} >"
