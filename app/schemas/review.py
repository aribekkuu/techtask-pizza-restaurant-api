from __future__ import annotations


from pydantic import BaseModel


class ReviewCreate(BaseModel):
    rating: int
    comment: str
    restaurant_id: int


class ReviewRead(BaseModel):
    id: int
    rating: int
    comment: str
    restaurant_name: str
