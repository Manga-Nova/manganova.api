from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modules.base.table import BaseTable
from src.modules.title.enums import TitleContentTypeEnum

if TYPE_CHECKING:
    from src.modules.tag.table import TagTable


class TitleTable(BaseTable):
    """Title model."""

    __tablename__ = "db_titles"

    name: Mapped[str] = mapped_column(__type_pos=String(500), unique=True)
    description: Mapped[str] = mapped_column(__type_pos=String(2000), nullable=True)
    release_date: Mapped[datetime | None] = mapped_column(
        __type_pos=DateTime(timezone=True),
        nullable=True,
    )
    content_type: Mapped[TitleContentTypeEnum] = mapped_column(__type_pos=String(100))

    tags: Mapped[list["TagTable"]] = relationship(
        "TagTable",
        secondary="db_title_tags",
        back_populates="titles",
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"< Title id={self.id} name={self.name} >"


class TitleTagTable(BaseTable):
    """Title tag model."""

    __tablename__ = "db_title_tags"

    title_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_titles.id", ondelete="CASCADE"),
        primary_key=True,
    )

    tag_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_tags.id", ondelete="CASCADE"),
        primary_key=True,
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return (
            f"< TitleTag id={self.id} "
            f"title_id={self.title_id} tag_id={self.tag_id} >"
        )
