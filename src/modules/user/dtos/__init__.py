from datetime import datetime

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

    id: str
    created_at: datetime
    updated_at: datetime
    username: str
    email: str
