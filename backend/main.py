from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.game_router import router as game_router
from backend.config import CORS_ORIGINS

# Database initialization
from backend.database import engine, Base
from backend.models import core # Ensure models are loaded for table creation
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mogul Blocks", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router, prefix="/api")
