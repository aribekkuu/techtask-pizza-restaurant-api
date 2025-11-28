from fastapi import FastAPI

from core.db import AsyncSessionMaker, init_db
from routers.routes import router as api_router
from services.seed import seed_data


app = FastAPI(title="Pizza Task API (Clean Architecture)", version="2.0.0")


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    async with AsyncSessionMaker() as session:
        await seed_data(session)


app.include_router(api_router)

