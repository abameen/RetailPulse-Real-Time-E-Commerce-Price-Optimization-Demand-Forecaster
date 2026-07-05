from fastapi import FastAPI

from app.api.api import api_router
from app.db.base import Base
from app.db.database import engine

app = FastAPI(title="RetailPulse")

# Creates tables based on your SQLAlchemy models if they don't already exist.
# Fine for now -- swap for Alembic migrations once the schema stabilizes.
Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "RetailPulse API is running"}
