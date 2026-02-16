from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.services.news.importer import import_scraped_articles_core

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/import-scraped")
def import_scraped_articles():
    response = import_scraped_articles_core()
    return {"total_processed": len(response), "details": response}
