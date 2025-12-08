from fastapi import APIRouter

from app.routers import pizza_router, restaurant_router, review_router

router = APIRouter()

router.include_router(pizza_router.router, tags=["pizzas"])
router.include_router(restaurant_router.router, tags=["restaurants"])
router.include_router(review_router.router, tags=["reviews"])