from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import asyncio


from app.routes.base_routes import router as base_router
from app.routes.articles import router as articles_router
from app.routes import embeddings as embeddings_router
from app.routes import search as search_router
from app.routes.cleanup_stats import router as cleanup_router
from app.routes.cleanup_old_news import router as cleanup_old_news_router
from app.routes.news_analysis_route import router as news_analysis_router
from app.routes.news_feed_route import router as news_feed_router
from app.scrapers.cryptoslate_scraper.scraper import scrape_latest_news


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Crypto News AI Backend", version="1.0.0", lifespan=lifespan)

app.include_router(embeddings_router.router)
app.include_router(base_router)
app.include_router(articles_router, prefix="/articles", tags=["Articles"])
app.include_router(search_router.router)
app.include_router(cleanup_old_news_router)
app.include_router(cleanup_router)
app.include_router(news_analysis_router, prefix="/api")
app.include_router(news_feed_router, prefix="/api")


# ✅ Temporary Debug Route
@app.post("/debug/run-scraper", tags=["Debug"])
async def debug_run_scraper():
    try:
        saved = await asyncio.to_thread(scrape_latest_news)
        return {"status": "ok", "articles_saved": saved}
    except Exception as e:
        return {"status": "error", "message": str(e)}
