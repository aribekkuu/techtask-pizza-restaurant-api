from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class Chef(Base):
    __tablename__ = "chefs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    restaurants: Mapped[List["Restaurant"]] = relationship(back_populates="chef")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    chef_id: Mapped[int] = mapped_column(ForeignKey("chefs.id"))

    chef: Mapped[Chef] = relationship(back_populates="restaurants")
    pizzas: Mapped[List["Pizza"]] = relationship(back_populates="restaurant")
    reviews: Mapped[List["Review"]] = relationship(back_populates="restaurant")


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


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int]
    comment: Mapped[str]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))

    restaurant: Mapped[Restaurant] = relationship(back_populates="reviews")


