# RetailPulse Backend

This repository contains a FastAPI backend service for RetailPulse.

## Database schema creation

The backend currently uses SQLAlchemy's `Base.metadata.create_all(bind=engine)` at startup to create tables automatically. There is no Alembic or separate migration tool configured in this repo yet.

If you add new models, they will be created when the FastAPI app starts and connects to the configured database.

## Run locally

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```
