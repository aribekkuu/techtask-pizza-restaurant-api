from __future__ import annotations

from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.pizza import Ingredient, Pizza
from app.schemas.pizza import IngredientRead, PizzaCreate, PizzaRead, PizzaUpdate


def pizzas_to_schema(pizzas: List[Pizza]) -> List[PizzaRead]:
    return [
        PizzaRead(
            id=pizza.id,
            name=pizza.name,
            cheese=pizza.cheese,
            dough=pizza.dough,
            secret=pizza.secret,
            restaurant_id=pizza.restaurant_id,
            restaurant_name=pizza.restaurant.name,
            ingredients=[
                IngredientRead.model_validate(ing) for ing in pizza.ingredients
            ],
        )
        for pizza in pizzas
    ]


async def fetch_ingredients(ids: List[int], session: AsyncSession) -> List[Ingredient]:
    if not ids:
        return []
    result = await session.execute(select(Ingredient).where(Ingredient.id.in_(ids)))
    ingredients = result.scalars().all()
    if len(ingredients) != len(set(ids)):
        raise HTTPException(status_code=404, detail="One or more ingredients not found")
    return ingredients


async def list_pizzas(session: AsyncSession) -> List[PizzaRead]:
    result = await session.execute(
        select(Pizza)
        .options(selectinload(Pizza.restaurant))
        .options(selectinload(Pizza.ingredients))
    )
    pizzas = result.scalars().unique().all()
    return pizzas_to_schema(pizzas)


async def create_pizza(payload: PizzaCreate, session: AsyncSession) -> PizzaRead:
    from app.models.restaurant import Restaurant  # local to avoid cycles

    restaurant = await session.get(Restaurant, payload.restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    ingredients = await fetch_ingredients(payload.ingredient_ids, session)
    pizza = Pizza(
        name=payload.name,
        cheese=payload.cheese,
        dough=payload.dough,
        secret=payload.secret,
        restaurant_id=payload.restaurant_id,
        ingredients=ingredients,
    )
    session.add(pizza)
    await session.commit()
    await session.refresh(pizza)
    return pizzas_to_schema([pizza])[0]


async def update_pizza(
    pizza_id: int, payload: PizzaUpdate, session: AsyncSession
) -> PizzaRead:
    from app.models.restaurant import Restaurant  # local to avoid cycles

    pizza = await session.get(
        Pizza,
        pizza_id,
        options=[selectinload(Pizza.ingredients), selectinload(Pizza.restaurant)],
    )
    if pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")

    data = payload.model_dump(exclude_unset=True)
    ingredient_ids = data.pop("ingredient_ids", None)

    if restaurant_id := data.get("restaurant_id"):
        restaurant = await session.get(Restaurant, restaurant_id)
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")

    for field, value in data.items():
        setattr(pizza, field, value)

    if ingredient_ids is not None:
        pizza.ingredients = await fetch_ingredients(ingredient_ids, session)

    await session.commit()
    await session.refresh(pizza)
    return pizzas_to_schema([pizza])[0]


async def delete_pizza(pizza_id: int, session: AsyncSession) -> None:
    pizza = await session.get(Pizza, pizza_id)
    if pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    await session.delete(pizza)
    await session.commit()
