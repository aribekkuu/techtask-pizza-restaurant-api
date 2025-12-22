from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    chef_id: Mapped[int] = mapped_column(ForeignKey("chefs.id"))

    chef: Mapped[Chef] = relationship(back_populates="restaurants")
    pizzas: Mapped[List["Pizza"]] = relationship(back_populates="restaurant")
    reviews: Mapped[List["Review"]] = relationship(back_populates="restaurant")


class Chef(Base):
    __tablename__ = "chefs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    restaurants: Mapped[List["Restaurant"]] = relationship(back_populates="chef")
