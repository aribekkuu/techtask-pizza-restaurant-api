from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.core.db import AsyncSessionMaker, init_db
from fastapi.middleware.cors import CORSMiddleware
from app.routers.main_router import router as api_router
from app.services.seed import seed_data
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    async with AsyncSessionMaker() as session:
        await seed_data(session)
    yield


app = FastAPI(
    title="Pizza Task API (Clean Architecture)", version="2.0.0", lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # потом лучше ограничить
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(api_router)
