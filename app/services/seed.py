from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pizza import Ingredient, Pizza
from app.models.restaurant import Restaurant, Chef
from app.models.review import Review


async def seed_data(session: AsyncSession) -> None:
    """ЗАПОЛНЕНИЕ БДШКИ ТЕСТОВЫМИ ДАННЫМИ"""
    from sqlalchemy import func, select

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


