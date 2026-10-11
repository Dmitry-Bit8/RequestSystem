from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine, SessionLocal
from src.models import Category
from src.routers import (
    auth, requests, users, statuses, categories, comments, health, reports,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    Base.metadata.create_all(bind=engine)

   
    db = SessionLocal()
    try:
        if not db.query(Category).first():
            db.add_all([
                Category(name="Оборудование",   sla_hours=24),
                Category(name="ПО и лицензии",  sla_hours=48),
                Category(name="Доступы",        sla_hours=8),
            ])
            db.commit()
            print("✅ Справочник категорий засеян")
        else:
            print("ℹ️ Категории уже есть — сев пропущен")
    finally:
        db.close()

    yield 


app = FastAPI(
    title="HelpDesk API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(requests.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(statuses.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "HelpDesk API работает!", "docs": "/docs", "health": "/health"}
