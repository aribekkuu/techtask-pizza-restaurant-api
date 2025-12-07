from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session

from app.models.pizza import Pizza, PizzaIngredient, Ingredient
from app.models.restaurant import Restaurant, Chef
from app.models.review import Review

from app.schemas.pizza import PizzaCreate, PizzaRead, PizzaUpdate, IngredientRead
from app.schemas.restaurant import RestaurantCreate, RestaurantRead, ChefCreate, ChefRead
from app.schemas.review import ReviewCreate, ReviewRead

from app.services.review import review_service
from app.services.pizza import pizza_service
from app.services.restaurant import restaurant_service

router = APIRouter()


SessionDep = Depends(get_session)

@router.post(
    "/restaurants/",
    response_model=RestaurantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_restaurant(
    payload: RestaurantCreate, session: AsyncSession = SessionDep
) -> RestaurantRead:
    return await restaurant_service.create_restaurant(payload, session)


@router.get("/restaurants/", response_model=list[RestaurantRead])
async def list_restaurants(session: AsyncSession = SessionDep) -> list[RestaurantRead]:
    return await restaurant_service.list_restaurants(session)

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