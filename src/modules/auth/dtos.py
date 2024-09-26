from pydantic import BaseModel

from src.modules.user.dtos import ExportUserDTO


class LoginParams(BaseModel):
    """Login parameters."""

    email: str
    password: str
    stay_logged_in: bool = False


class RegisterParams(BaseModel):
    """Register parameters."""

    username: str
    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response."""

    access_token: str
    user: ExportUserDTO


class ChangePasswordParams(BaseModel):
    """Change password parameters."""

    old_password: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    """Change password parameters."""

    message: str = "Password changed successfully"


class Payload(BaseModel):
    """Payload model."""

    user_id: int
    email: str
    username: str
    stay_logged_in: bool
