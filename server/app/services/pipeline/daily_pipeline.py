import asyncio
from app.database.database import SessionLocal
import logging
from app.models.news.news_article import NewsArticle
from app.services.pipeline.process_article import process_article
from app.scrapers.cryptoslate_scraper.scraper import scrape_latest_news
from app.services.ai.backfill_embedding_core import backfill_embeddings_core
from app.services.news.importer import import_scraped_articles_core


logger = logging.getLogger(__name__)


async def process_daily_news():
    logger.info("🚀 Daily News Pipeline Started")

    try:
        logger.info("🕸 Starting scraper...")
        scrape_latest_news()
    except Exception as e:
        logger.error(f"❌ Scraper failed: {e}")

    # STEP 1 — Import scraped articles
    with SessionLocal() as db:
        logger.info("📥 Importing scraped articles...")
        await import_scraped_articles_core(db)

    # STEP 2 — Generate embeddings (RUN OUTSIDE EVENT LOOP)
    logger.info("🧠 Generating embeddings...")
    await asyncio.to_thread(backfill_embeddings_core)

    # STEP 3 — Fetch articles to analyze
    with SessionLocal() as db:
        new_article_ids = [
            a.id
            for a in db.query(NewsArticle.id)
            .filter(NewsArticle.is_analyzed == False)
            .all()
        ]

    logger.info(f"📝 Found {len(new_article_ids)} new articles to analyze.")

    # STEP 4 — Process articles (session per article)
    for article_id in new_article_ids:
        logger.info(f"🔍 Processing article ID={article_id}")
        await process_article(article_id)

    logger.info("✅ Daily News Pipeline Completed Successfully")
