from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.db.base import Base
from app.db.database import engine

app = FastAPI(title="RetailPulse")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creates tables based on your SQLAlchemy models if they don't already exist.
# Fine for now -- swap for Alembic migrations once the schema stabilizes.
Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "RetailPulse API is running"}
