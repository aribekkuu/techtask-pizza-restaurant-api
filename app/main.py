from fastapi import FastAPI

from app.core.db import AsyncSessionMaker, init_db
from app.routers.routes import router as api_router
from app.services.seed import seed_data


app = FastAPI(title="Pizza Task API (Clean Architecture)", version="2.0.0")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    async with AsyncSessionMaker() as session:
        await seed_data(session)


app.include_router(api_router)

