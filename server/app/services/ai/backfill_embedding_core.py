from app.database.database import SessionLocal
from app.services.ai.embedding_pipeline import backfill_article_embeddings


def backfill_embeddings_core():
    db = SessionLocal()
    try:
        backfill_article_embeddings(db, limit=100)
    finally:
        db.close()
    return {"status": "completed"}
