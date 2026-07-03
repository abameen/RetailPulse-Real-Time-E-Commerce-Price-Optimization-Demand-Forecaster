from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base

settings = get_settings()

# The engine manages the actual connection pool to Postgres
engine = create_engine(settings.DATABASE_URL)

# SessionLocal is a factory for creating new DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function used by FastAPI routes.
    Opens a session, yields it for use, then closes it afterward
    -- even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
