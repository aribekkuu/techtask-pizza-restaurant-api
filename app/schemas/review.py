from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    rating: int
    comment: str
    restaurant_id: int


class ReviewRead(BaseModel):
    id: int
    rating: int
    comment: str
    restaurant_name: str