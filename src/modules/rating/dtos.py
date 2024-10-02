from typing import Literal

from pydantic import BaseModel


class Rating(BaseModel):
    """Rating model."""

    average: float
    ratings: dict[int, int]


class CreateRating(BaseModel):
    """Create rating model."""

    user_id: int
    title_id: int
    value: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class PostRating(BaseModel):
    """Create rating model."""

    value: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
