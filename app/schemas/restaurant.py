from __future__ import annotations

from typing import Optional

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
