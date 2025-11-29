from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import hashlib

from app.models.news.news_article import NewsArticle


def compute_hash(title: str, url: str, content: str) -> str:
    combined = f"{title}::{url}::{content}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def insert_article(
    db: Session,
    title: str,
    url: str,
    content: str,
    category: str,
):
    try:
        # Compute deterministic hash based on stable input fields
        article_hash = compute_hash(title, url, content)

        # Check for duplicates by url or hash
        existing = (
            db.query(NewsArticle)
            .filter((NewsArticle.url == url) | (NewsArticle.hash == article_hash))
            .first()
        )

        if existing:
            return {"status": "exists", "id": existing.id}

        # Insert new record
        new_article = NewsArticle(
            title=title,
            url=url,
            content=content,
            category=category,
            hash=article_hash,
            created_at=datetime.utcnow(),
            is_relevant=1,
            published_at=None,
        )

        db.add(new_article)
        db.commit()
        db.refresh(new_article)

        return {"status": "inserted", "id": new_article.id}

    except IntegrityError as e:
        db.rollback()
        return {"status": "duplicate", "error": str(e)}

    except Exception as e:
        db.rollback()
        return {"status": "error", "error": str(e)}
