from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    articles_count = db.execute(text("SELECT COUNT(*) FROM news_articles;")).scalar()
    embeddings_count = db.execute(text("SELECT COUNT(*) FROM embeddings;")).scalar()
    return {"articles": articles_count, "embeddings": embeddings_count}
