from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.articles import get_db
from app.models.news.news_article import NewsArticle

router = APIRouter()


@router.get("/news")
def get_news_feed(limit: int = 45, db: Session = Depends(get_db)):
    articles = (
        db.query(NewsArticle)
        .filter(NewsArticle.is_analyzed == True)
        .order_by(NewsArticle.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "last_updated": articles[0].created_at if articles else None,
        "data": [
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "category": article.category,
                "published_at": article.published_at,
                "analysis": {
                    "prediction": (
                        article.analysis[0].prediction if article.analysis else None
                    ),
                },
            }
            for article in articles
        ],
    }
