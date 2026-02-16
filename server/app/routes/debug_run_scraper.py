import asyncio
from app.scrapers.cryptoslate_scraper.scraper import scrape_latest_news
from server import app


@app.post("/debug/run-scraper", tags=["Debug"])
async def debug_run_scraper():
    try:
        saved = await asyncio.to_thread(scrape_latest_news)
        return {"status": "ok", "articles_saved": saved}
    except Exception as e:
        return {"status": "error", "message": str(e)}
