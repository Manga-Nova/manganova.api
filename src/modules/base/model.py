from sqlalchemy.orm import DeclarativeBase


class ModelBase(DeclarativeBase):
    """Base model for all models."""

    """
    # Example of a base model with common columns.
    # This is commented because sqlalchemy does not organize the columns according to
    # class inheritance, all classes that inherit from ModelBase would have the
    # ModelBase parameters as the last items in the table instead of the first items

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(ZoneInfo("UTC")))
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=datetime.now(ZoneInfo("UTC")),
        nullable=True,
    )
    """
