from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import AsyncSessionMaker, init_db
from app.routers.main_router import router as api_router
from app.services.seed import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    async with AsyncSessionMaker() as session:
        await seed_data(session)
    yield


app = FastAPI(title="Pizza Task API (Clean Architecture)", version="2.0.0", lifespan=lifespan)

app.include_router(api_router)

