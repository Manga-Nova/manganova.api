from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.base.model import ModelBaseTable


class RatingTable(ModelBaseTable):
    __tablename__ = "db_ratings"

    user_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    title_id: Mapped[int] = mapped_column(
        __type_pos=ForeignKey("db_titles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    value: Mapped[float]

    def __repr__(self) -> str:
        return (
            f"< Rating id={self.id} user_id={self.user_id} "
            f"title_id={self.title_id} value={self.value} >"
        )
