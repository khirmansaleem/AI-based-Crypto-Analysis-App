from sqlalchemy.orm import Session
from app.models.news.news_article import NewsArticle
from app.models.news.embedding import Embedding
from app.services.ai.embeddings import get_embedding


def backfill_article_embeddings(db: Session, limit: int = 100):
    # Find articles that have no embedding yet
    articles = (
        db.query(NewsArticle)
        .outerjoin(Embedding, Embedding.article_id == NewsArticle.id)
        .filter(Embedding.id.is_(None))
        .limit(limit)
        .all()
    )

    created = 0

    for article in articles:
        text = f"{article.title}\n\n{article.content}"
        vector = get_embedding(text)

        embedding_row = Embedding(
            article_id=article.id,
            embedding=vector,
        )

        db.add(embedding_row)
        created += 1

    db.commit()
    return created
