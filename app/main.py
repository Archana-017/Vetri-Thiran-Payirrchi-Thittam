from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import init_db
from app.routers import auth, planners, pages

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)

@app.get("/health")
def health(): return {"status":"ok","service":"PocketSmart AI"}
