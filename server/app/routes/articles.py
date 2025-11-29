import os
import shutil
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.services.load_scraped_articles import load_all_scraped_articles
from app.services.article_service import insert_article

router = APIRouter()

SCRAPED_DIR = "app/scrapers/scraped_articles"
PROCESSED_DIR = "app/scrapers/scraped_articles/processed"

# Make sure processed folder exists
os.makedirs(PROCESSED_DIR, exist_ok=True)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/import-scraped")
def import_scraped_articles(db: Session = Depends(get_db)):
    """
    Reads TXT files from scraped_articles/, parses them,
    inserts them into PostgreSQL, and moves processed files
    to scraped_articles/processed/.
    """

    articles = load_all_scraped_articles()

    response = []

    for art in articles:

        # Insert into DB
        result = insert_article(
            db=db,
            title=art["title"],
            url=art["url"],
            content=art["content"],
            category=art["category"],
        )

        # Append result for API response
        response.append(
            {
                "file": art["filename"],
                "status": result["status"],
                "id": result.get("id"),
                "error": result.get("error"),
            }
        )

        # Move file to processed/ only if inserted or existed
        if result["status"] in ("inserted", "exists"):
            shutil.move(art["filepath"], os.path.join(PROCESSED_DIR, art["filename"]))

    return {"total_processed": len(response), "details": response}
