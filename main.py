from __future__ import annotations
from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey, func, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, selectinload


DB_URL = "sqlite+aiosqlite:///./techtask.db"
engine = create_async_engine(DB_URL, echo=False)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


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


async def get_session() -> Annotated[AsyncSession, Depends]:
    async with AsyncSessionMaker() as session:
        yield session


app = FastAPI(title="Pizza Task API", version="1.0.0")


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionMaker() as session:
        await seed_data(session)


async def seed_data(session: AsyncSession) -> None:
    restaurant_count = await session.scalar(select(func.count(Restaurant.id)))
    if restaurant_count and restaurant_count > 0:
        return

    chefs = [
        Chef(name="Марио Братишкин", email="mario@example.com"),
        Chef(name="Гордон Рамзаев", email="gordon@example.com"),
        Chef(name="Виталик Пиццайоло", email="vitalik@example.com"),
    ]
    session.add_all(chefs)
    await session.flush()

    restaurants = [
        Restaurant(name="LoLoPizza", address="Байтурсынова 80", chef_id=chefs[0].id),
        Restaurant(name="PizzaHubovich", address="Сейфуллина 500", chef_id=chefs[1].id),
        Restaurant(name="Доминошка", address="пр. Абая 150/1", chef_id=chefs[2].id),
    ]
    session.add_all(restaurants)
    await session.flush()

    ingredient_names = {
        "Моцарелла",
        "Тонкое тесто",
        "Экстракт грейпфрутовых косточек",
        "Чеддер",
        "Пышное тесто",
        "Слезы программистов",
        "Микс четырех сыров",
        "Классическое тесто",
        "Магия итальянских бабушек",
        "Томаты",
        "Базилик",
    }
    ingredient_objs = {name: Ingredient(name=name) for name in ingredient_names}
    session.add_all(ingredient_objs.values())
    await session.flush()

    def pick(names: List[str]) -> List[Ingredient]:
        return [ingredient_objs[name] for name in names]

    pizzas = [
        Pizza(
            name="Margherita",
            cheese="Моцарелла",
            dough="тонкое",
            secret="экстракт грейпфрутовых косточек",
            restaurant_id=restaurants[0].id,
            ingredients=pick(["Моцарелла", "Тонкое тесто", "Томаты", "Базилик"]),
        ),
        Pizza(
            name="Дедлайн",
            cheese="Чеддер",
            dough="пышное",
            secret="слезы программистов",
            restaurant_id=restaurants[1].id,
            ingredients=pick(["Чеддер", "Пышное тесто", "Слезы программистов"]),
        ),
        Pizza(
            name="Четыре чиза",
            cheese="Микс четырех сыров",
            dough="классическое",
            secret="магия итальянских бабушек",
            restaurant_id=restaurants[2].id,
            ingredients=pick(
                [
                    "Микс четырех сыров",
                    "Классическое тесто",
                    "Магия итальянских бабушек",
                ]
            ),
        ),
        Pizza(
            name="LoLo Special",
            cheese="Моцарелла",
            dough="тонкое",
            secret="extra virgin olive oil",
            restaurant_id=restaurants[0].id,
            ingredients=pick(["Моцарелла", "Тонкое тесто", "Томаты"]),
        ),
    ]
    session.add_all(pizzas)

    reviews = [
        Review(rating=5, comment="Лучшая пицца города!", restaurant_id=restaurants[0].id),
        Review(rating=4, comment="Очень вкусно, но долго ждали.", restaurant_id=restaurants[1].id),
    ]
    session.add_all(reviews)
    await session.commit()


@app.get("/restaurants/", response_model=List[RestaurantRead])
async def list_restaurants(session: AsyncSession = Depends(get_session)) -> List[Restaurant]:
    result = await session.execute(select(Restaurant).options(selectinload(Restaurant.chef)))
    return result.scalars().unique().all()


@app.post(
    "/restaurants/",
    response_model=RestaurantRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_restaurant(
    payload: RestaurantCreate, session: AsyncSession = Depends(get_session)
) -> Restaurant:
    chef = await session.get(Chef, payload.chef_id)
    if chef is None:
        raise HTTPException(status_code=404, detail="Chef not found")

    restaurant = Restaurant(**payload.model_dump())
    session.add(restaurant)
    await session.commit()
    await session.refresh(restaurant)
    return restaurant


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
            ingredients=[IngredientRead.model_validate(ing) for ing in pizza.ingredients],
        )
        for pizza in pizzas
    ]


@app.get("/pizzas/", response_model=List[PizzaRead])
async def list_pizzas(session: AsyncSession = Depends(get_session)) -> List[PizzaRead]:
    result = await session.execute(
        select(Pizza)
        .options(selectinload(Pizza.restaurant))
        .options(selectinload(Pizza.ingredients))
    )
    pizzas = result.scalars().unique().all()
    return pizzas_to_schema(pizzas)


async def fetch_ingredients(ids: List[int], session: AsyncSession) -> List[Ingredient]:
    if not ids:
        return []
    result = await session.execute(select(Ingredient).where(Ingredient.id.in_(ids)))
    ingredients = result.scalars().all()
    if len(ingredients) != len(set(ids)):
        raise HTTPException(status_code=404, detail="One or more ingredients not found")
    return ingredients


@app.post("/pizzas/", response_model=PizzaRead, status_code=status.HTTP_201_CREATED)
async def create_pizza(
    payload: PizzaCreate, session: AsyncSession = Depends(get_session)
) -> PizzaRead:
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


@app.put("/pizzas/{pizza_id}", response_model=PizzaRead)
@app.patch("/pizzas/{pizza_id}", response_model=PizzaRead)
async def update_pizza(
    pizza_id: int, payload: PizzaUpdate, session: AsyncSession = Depends(get_session)
) -> PizzaRead:
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


@app.delete("/pizzas/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(pizza_id: int, session: AsyncSession = Depends(get_session)) -> None:
    pizza = await session.get(Pizza, pizza_id)
    if pizza is None:
        raise HTTPException(status_code=404, detail="Pizza not found")
    await session.delete(pizza)
    await session.commit()


@app.get("/chefs/", response_model=List[ChefRead])
async def list_chefs(session: AsyncSession = Depends(get_session)) -> List[Chef]:
    result = await session.execute(select(Chef))
    return result.scalars().all()


@app.post("/chefs/", response_model=ChefRead, status_code=status.HTTP_201_CREATED)
async def create_chef(payload: ChefCreate, session: AsyncSession = Depends(get_session)) -> Chef:
    chef = Chef(**payload.model_dump())
    session.add(chef)
    await session.commit()
    await session.refresh(chef)
    return chef


@app.get("/ingredients/", response_model=List[IngredientRead])
async def list_ingredients(session: AsyncSession = Depends(get_session)) -> List[Ingredient]:
    result = await session.execute(select(Ingredient))
    return result.scalars().all()


@app.get("/restaurants/{restaurant_id}/menu/", response_model=List[PizzaRead])
async def restaurant_menu(
    restaurant_id: int, session: AsyncSession = Depends(get_session)
) -> List[PizzaRead]:
    restaurant = await session.get(Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    result = await session.execute(
        select(Pizza)
        .where(Pizza.restaurant_id == restaurant_id)
        .options(selectinload(Pizza.ingredients))
        .options(selectinload(Pizza.restaurant))
    )
    pizzas = result.scalars().unique().all()
    return pizzas_to_schema(pizzas)


@app.get("/reviews/", response_model=List[ReviewRead])
async def list_reviews(session: AsyncSession = Depends(get_session)) -> List[ReviewRead]:
    result = await session.execute(
        select(Review, Restaurant.name.label("restaurant_name")).join(
            Restaurant, Review.restaurant_id == Restaurant.id
        )
    )
    return [
        ReviewRead(
            id=row.Review.id,
            rating=row.Review.rating,
            comment=row.Review.comment,
            restaurant_name=row.restaurant_name,
        )
        for row in result.all()
    ]


@app.post("/reviews/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    payload: ReviewCreate, session: AsyncSession = Depends(get_session)
) -> ReviewRead:
    restaurant = await session.get(Restaurant, payload.restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    review = Review(**payload.model_dump())
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return ReviewRead(
        id=review.id,
        rating=review.rating,
        comment=review.comment,
        restaurant_name=restaurant.name,
    )

