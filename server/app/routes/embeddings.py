from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.ai.embedding_pipeline import backfill_article_embeddings
from app.database.database import get_db

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


@router.post("/backfill")
def backfill_embeddings(limit: int = 100, db: Session = Depends(get_db)):
    created = backfill_article_embeddings(db, limit=limit)
    return {"created": created}
