from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session


from app.schemas.review import ReviewCreate, ReviewRead

from app.services.review import review_service


router = APIRouter()


SessionDep = Depends(get_session)


@router.get("/reviews/", response_model=list[ReviewRead])
async def list_reviews(session: AsyncSession = SessionDep) -> list[ReviewRead]:
    return await review_service.list_reviews(session)


@router.post(
    "/reviews/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED
)
async def create_review(
    payload: ReviewCreate, session: AsyncSession = SessionDep
) -> ReviewRead:
    return await review_service.create_review(payload, session)
