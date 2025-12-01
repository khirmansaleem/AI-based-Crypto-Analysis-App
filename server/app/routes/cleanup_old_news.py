from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()


@router.post("/cleanup-old-news")
def cleanup_old_news(db: Session = Depends(get_db)):
    # delete embeddings of articles older than 30 days
    db.execute(
        text(
            """
        DELETE FROM embeddings
        USING news_articles
        WHERE embeddings.article_id = news_articles.id
        AND news_articles.created_at < NOW() - INTERVAL '30 days';
    """
        )
    )

    # delete articles older than 30 days
    db.execute(
        text(
            """
        DELETE FROM news_articles
        WHERE created_at < NOW() - INTERVAL '30 days';
    """
        )
    )

    db.commit()
    return {"status": "success", "message": "Old news and embeddings deleted"}
