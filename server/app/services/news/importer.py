import os
import shutil
from requests import Session
from app.services.news.article_service import insert_article
from app.services.news.load_scraped_articles import load_all_scraped_articles
from app.services.news.paths import FAILED_DIR, PROCESSED_DIR


async def import_scraped_articles_core(db: Session):
    articles = load_all_scraped_articles()
    response = []

    for art in articles:
        result = await insert_article(
            db=db,
            title=art["title"],
            url=art["url"],
            content=art["content"],
            category=art["category"],
            published_at=art["published_at"],  # <-- NEW
        )

        response.append(
            {
                "file": art["filename"],
                "status": result["status"],
                "id": result.get("id"),
                "error": result.get("error"),
            }
        )

        # Move file to respective directory
        target_dir = (
            PROCESSED_DIR if result["status"] in ("inserted", "exists") else FAILED_DIR
        )
        shutil.move(art["filepath"], os.path.join(target_dir, art["filename"]))

    return response
