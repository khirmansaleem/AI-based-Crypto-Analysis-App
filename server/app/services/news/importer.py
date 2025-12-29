import os
import shutil
from fastapi import logger
from app.services.news.article_service import insert_article
from app.services.news.load_scraped_articles import load_all_scraped_articles
from app.services.news.paths import FAILED_DIR
from app.database.database import SessionLocal


def import_scraped_articles_core():
    articles = load_all_scraped_articles()
    response = []

    with SessionLocal() as db:
        for art in articles:
            result = insert_article(
                db=db,
                title=art["title"],
                url=art["url"],
                content=art["content"],
                category=art["category"],
                published_at=art["published_at"],
            )

            response.append(
                {
                    "file": art["filename"],
                    "status": result["status"],
                    "id": result.get("id"),
                    "error": result.get("error"),
                }
            )

            if result["status"] in ("inserted", "exists"):
                try:
                    os.remove(art["filepath"])
                except Exception as e:
                    logger.warning(f"Failed to delete {art['filepath']}: {e}")
            else:
                shutil.move(
                    art["filepath"],
                    os.path.join(FAILED_DIR, art["filename"]),
                )

        db.commit()

    return response
