from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ChefCreate(BaseModel):
    name: str
    email: Optional[str] = None


class ChefRead(ChefCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RestaurantCreate(BaseModel):
    name: str
    address: str
    chef_id: int


class RestaurantRead(RestaurantCreate):
    id: int
    chef: ChefRead

    model_config = ConfigDict(from_attributes=True)


class IngredientRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PizzaCreate(BaseModel):
    name: str
    cheese: str
    dough: str
    secret: str
    restaurant_id: int
    ingredient_ids: List[int]


class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    cheese: Optional[str] = None
    dough: Optional[str] = None
    secret: Optional[str] = None
    restaurant_id: Optional[int] = None
    ingredient_ids: Optional[List[int]] = None


class PizzaRead(BaseModel):
    id: int
    name: str
    cheese: str
    dough: str
    secret: str
    restaurant_id: int
    restaurant_name: str
    ingredients: List[IngredientRead]

    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    rating: int
    comment: str
    restaurant_id: int


class ReviewRead(BaseModel):
    id: int
    rating: int
    comment: str
    restaurant_name: str


