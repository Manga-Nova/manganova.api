from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    """Data Transfer Object for creating a user."""

    username: str
    email: str
    password: str


class UpdateUserDTO(BaseModel):
    """Data Transfer Object for updating a user."""

    username: str | None = None


class ExportUserDTO(BaseModel):
    """Data Transfer Object for exporting a user."""

    id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    username: str
    email: str
