from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src._utils import current_datetime

if TYPE_CHECKING:
    from pydantic import BaseModel


class ModelBaseTable(DeclarativeBase):
    """Base model for all models."""

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

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"<{self.__class__.__name__} id={self.id} >"

    def update(self, model: "BaseModel", exclude: set[str] | None = None) -> None:
        """Update the model with the given data."""
        for key, value in model.model_dump(
            exclude_defaults=True,
            exclude_unset=True,
            exclude=exclude,
        ).items():
            setattr(self, key, value)

    def model_dump(self) -> dict[str, Any]:
        """Return a dictionary representation of the model."""
        _return: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue

            _return[key] = value

            if isinstance(value, list):
                items: list[Any] = []
                item: Any
                for item in value:
                    if isinstance(item, ModelBaseTable):
                        items.append(item.model_dump())
                    else:
                        items.append(item)

                _return[key] = items
                continue

        return _return
