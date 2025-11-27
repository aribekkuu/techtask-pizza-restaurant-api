from __future__ import annotations

from typing import List

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.models import Chef, Restaurant
from src.schemas import RestaurantCreate, RestaurantRead


async def list_restaurants(session: AsyncSession) -> List[RestaurantRead]:
    result = await session.execute(
        select(Restaurant).options(selectinload(Restaurant.chef))
    )
    restaurants = result.scalars().unique().all()
    return [RestaurantRead.model_validate(r) for r in restaurants]


async def create_restaurant(
    payload: RestaurantCreate, session: AsyncSession
) -> RestaurantRead:
    chef = await session.get(Chef, payload.chef_id)
    if chef is None:
        raise HTTPException(status_code=404, detail="Chef not found")

    restaurant = Restaurant(**payload.model_dump())
    session.add(restaurant)
    await session.commit()
    await session.refresh(restaurant)
    return RestaurantRead.model_validate(restaurant)


async def count_restaurants(session: AsyncSession) -> int:
    return await session.scalar(select(func.count(Restaurant.id))) or 0


