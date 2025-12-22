from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


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


class IngredientRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
