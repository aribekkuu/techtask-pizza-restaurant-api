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

@router.get("/ingredients/", response_model=list[IngredientRead])
async def list_ingredients(
    session: AsyncSession = SessionDep,
) -> list[IngredientRead]:
    result = await session.execute(Ingredient.__table__.select())
    ingredients = result.scalars().all()
    return [IngredientRead.model_validate(i) for i in ingredients]