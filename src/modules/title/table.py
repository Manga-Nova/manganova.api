from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src._utils import current_datetime
from src.modules.base.table import BaseTable
from src.modules.title.enums import TitleContentTypeEnum

if TYPE_CHECKING:
    from src.modules.tag.table import TagTable


class TitleTable(BaseTable):
    """Title model."""

    __tablename__ = "db_titles"

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
        return f"< TitleTag title_id={self.title_id} tag_id={self.tag_id} >"


class TitleRatingTable(BaseTable):
    __tablename__ = "db_title_ratings"

    user_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    target_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_titles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    value: Mapped[float]

    def __repr__(self) -> str:
        return (
            f"< TitleRating user_id={self.user_id} "
            f"title_id={self.target_id} value={self.value} >"
        )
