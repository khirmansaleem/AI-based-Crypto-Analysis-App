from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from dateutil import parser as dateparser
import hashlib
from app.services.deepseek_client.summarizer import (
    generate_summary,
)  # <-- ADD THIS IMPORT
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
    published_at: str = None,  # <-- NEW PARAMETER
):
    try:
        # Compute deterministic hash
        article_hash = compute_hash(title, url, content)

        # Duplicate check
        existing = (
            db.query(NewsArticle)
            .filter((NewsArticle.url == url) | (NewsArticle.hash == article_hash))
            .first()
        )

        if existing:
            return {"status": "exists", "id": existing.id}

        # --- Convert PublishedAt safely ---
        pub_datetime = None
        if published_at:
            try:
                pub_datetime = dateparser.parse(published_at)
            except Exception:
                pub_datetime = None  # failsafe

        # --- Generate LLM summary (async) ---
        content_summary = generate_summary(content, pub_datetime)
        summary = f"{title}. {content_summary}"

        # --- Create new DB row ---
        new_article = NewsArticle(
            title=title,
            url=url,
            content=content,
            summary=summary,
            category=category,
            hash=article_hash,
            created_at=datetime.utcnow(),
            published_at=pub_datetime,  # <-- NOW STORED
            is_relevant=1,
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
