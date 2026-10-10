from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base, engine
from src.seed import seed
from src.routers import (
    auth, requests, users, statuses, 
    categories, comments, health, reports
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HelpDesk API",
    description="API системы учёта заявок (ЛР №6-8)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(requests.router)
app.include_router(users.router)
app.include_router(statuses.router)
app.include_router(categories.router)
app.include_router(comments.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "message": "HelpDesk API работает!",
        "docs": "/docs",
        "health": "/health"
    }

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
   
