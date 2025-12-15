from app.database.database import SessionLocal
import logging

# from app.services.ai.backfill_embedding_core import backfill_embeddings_core
# from app.services.news.importer import import_scraped_articles_core
from app.models.news.news_article import NewsArticle
from app.services.pipeline.process_article import process_article
from app.scrapers.cryptoslate_scraper.scraper import scrape_latest_news
from app.services.ai.backfill_embedding_core import backfill_embeddings_core
from app.services.news.importer import import_scraped_articles_core


logger = logging.getLogger(__name__)


async def process_daily_news():
    """
    This function is called daily by the scheduler.
    It handles the full daily pipeline:
    1. Import scraped TXT files
    2. Generate embeddings
    3. Analyze unprocessed articles
    """

    logger.info("🚀 Daily News Pipeline Started")

    # ---------------------------
    # STEP 0 — SCRAPE LATEST NEWS
    # ---------------------------

    try:
        logger.info("🕸 Starting scraper...")
        count = scrape_latest_news()
        logger.info(f"📰 Scraper finished — {count} new articles saved as TXT")
    except Exception as e:
        logger.error(f"❌ Scraper failed: {e}")
        # We continue — maybe older TXT still exist

    db = SessionLocal()

    try:
        # STEP 1 — Import scraped articles
        logger.info("📥 Importing scraped articles...")
        await import_scraped_articles_core(db)

        # STEP 2 — Generate embeddings for new articles
        logger.info("🧠 Generating embeddings...")
        backfill_embeddings_core()

        # STEP 3 — Fetch all articles that are not analyzed yet
        new_articles = (
            db.query(NewsArticle).filter(NewsArticle.is_analyzed == False).all()
        )

        logger.info(f"📝 Found {len(new_articles)} new articles to analyze.")

        # STEP 4 — Process each article
        for article in new_articles:
            logger.info(f"🔍 Processing article ID={article.id}")
            await process_article(db, article.id)

        logger.info("✅ Daily News Pipeline Completed Successfully")

    except Exception as e:
        logger.error(f"❌ Error in daily pipeline: {e}", exc_info=True)

    finally:
        db.close()
