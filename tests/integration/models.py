from datetime import datetime
from typing import TypedDict


class UserModel(TypedDict):
    id: int
    created_at: datetime
    username: str
    email: str


class AuthResponse(TypedDict):
    access_token: str
    user: UserModel
