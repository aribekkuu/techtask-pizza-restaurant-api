from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models.models import Chef, Ingredient, Pizza, Restaurant
from app.schemas import (
    ChefCreate,
    ChefRead,
    IngredientRead,
    PizzaCreate,
    PizzaRead,
    PizzaUpdate,
    RestaurantCreate,
    RestaurantRead,
    ReviewCreate,
    ReviewRead,
)
from app.services import pizza_service, restaurant_service, review_service


router = APIRouter()


SessionDep = Depends(get_session)


@router.get("/restaurants/", response_model=list[RestaurantRead])
async def list_restaurants(session: AsyncSession = SessionDep) -> list[RestaurantRead]:
    return await restaurant_service.list_restaurants(session)


@router.post(
    "/restaurants/",
    response_model=RestaurantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_restaurant(
    payload: RestaurantCreate, session: AsyncSession = SessionDep
) -> RestaurantRead:
    return await restaurant_service.create_restaurant(payload, session)


@router.get("/pizzas/", response_model=list[PizzaRead])
async def list_pizzas(session: AsyncSession = SessionDep) -> list[PizzaRead]:
    return await pizza_service.list_pizzas(session)


@router.post("/pizzas/", response_model=PizzaRead, status_code=status.HTTP_201_CREATED)
async def create_pizza(
    payload: PizzaCreate, session: AsyncSession = SessionDep
) -> PizzaRead:
    return await pizza_service.create_pizza(payload, session)


@router.put("/pizzas/{pizza_id}", response_model=PizzaRead)
@router.patch("/pizzas/{pizza_id}", response_model=PizzaRead)
async def update_pizza(
    pizza_id: int, payload: PizzaUpdate, session: AsyncSession = SessionDep
) -> PizzaRead:
    return await pizza_service.update_pizza(pizza_id, payload, session)


@router.delete("/pizzas/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(pizza_id: int, session: AsyncSession = SessionDep) -> None:
    await pizza_service.delete_pizza(pizza_id, session)


@router.get("/chefs/", response_model=list[ChefRead])
async def list_chefs(session: AsyncSession = SessionDep) -> list[ChefRead]:
    result = await session.execute(Chef.__table__.select())
    chefs = result.scalars().all()
    return [ChefRead.model_validate(c) for c in chefs]


@router.post("/chefs/", response_model=ChefRead, status_code=status.HTTP_201_CREATED)
async def create_chef(
    payload: ChefCreate, session: AsyncSession = SessionDep
) -> ChefRead:
    chef = Chef(**payload.model_dump())
    session.add(chef)
    await session.commit()
    await session.refresh(chef)
    return ChefRead.model_validate(chef)


@router.get("/ingredients/", response_model=list[IngredientRead])
async def list_ingredients(
    session: AsyncSession = SessionDep,
) -> list[IngredientRead]:
    result = await session.execute(Ingredient.__table__.select())
    ingredients = result.scalars().all()
    return [IngredientRead.model_validate(i) for i in ingredients]


@router.get("/restaurants/{restaurant_id}/menu/", response_model=list[PizzaRead])
async def restaurant_menu(
    restaurant_id: int, session: AsyncSession = SessionDep
) -> list[PizzaRead]:
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    result = await session.execute(
        select(Pizza)
        .where(Pizza.restaurant_id == restaurant_id)
        .options(selectinload(Pizza.ingredients))
        .options(selectinload(Pizza.restaurant))
    )
    pizzas = result.scalars().unique().all()
    return pizza_service.pizzas_to_schema(pizzas)


@router.get("/reviews/", response_model=list[ReviewRead])
async def list_reviews(session: AsyncSession = SessionDep) -> list[ReviewRead]:
    return await review_service.list_reviews(session)


@router.post("/reviews/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate, session: AsyncSession = SessionDep
) -> ReviewRead:
    return await review_service.create_review(payload, session)


