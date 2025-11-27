from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Restaurant, Review
from src.schemas import ReviewCreate, ReviewRead


async def list_reviews(session: AsyncSession) -> List[ReviewRead]:
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


async def create_review(
    payload: ReviewCreate, session: AsyncSession
) -> ReviewRead:
    restaurant = await session.get(Restaurant, payload.restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

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


