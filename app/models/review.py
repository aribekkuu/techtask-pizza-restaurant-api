from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

from app.models.restaurant import Restaurant

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int]
    comment: Mapped[str]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))

    restaurant: Mapped[Restaurant] = relationship(back_populates="reviews")