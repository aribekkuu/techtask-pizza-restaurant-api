from fastapi import APIRouter, Depends, status
from app.core.db import get_session

router = APIRouter()


SessionDep = Depends(get_session)