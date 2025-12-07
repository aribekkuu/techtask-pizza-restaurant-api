from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

from app.core.db import Base
from app.models.restaurant import Restaurant, Chef
from app.models.review import Review

class Pizza(Base):
    __tablename__ = "pizzas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cheese: Mapped[str]
    dough: Mapped[str]
    secret: Mapped[str]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))

    restaurant: Mapped[Restaurant] = relationship(back_populates="pizzas")
    ingredients: Mapped[List[Ingredient]] = relationship(
        secondary="pizzas_ingredients", back_populates="pizzas"
    )

class PizzaIngredient(Base):
    __tablename__ = "pizzas_ingredients"

    pizza_id: Mapped[int] = mapped_column(
        ForeignKey("pizzas.id"), primary_key=True, index=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"), primary_key=True, index=True
    )

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    pizzas: Mapped[List["Pizza"]] = relationship(
        secondary="pizzas_ingredients", back_populates="ingredients"
    )