from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.routes.base_routes import router as base_router
from app.routes.articles import router as articles_router
from app.routes import embeddings as embeddings_router
from app.routes import search as search_router
from app.routes.cleanup_stats import router as cleanup_router
from app.routes.cleanup_old_news import router as cleanup_old_news_router
from app.routes.news_analysis_route import router as news_analysis_router
from app.scheduler.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    start_scheduler()
    print("Scheduler started (lifespan)")

    yield  # FastAPI now handles requests

    # --- Shutdown ---
    stop_scheduler()
    print("Scheduler stopped (lifespan)")


app = FastAPI(title="Crypto News AI Backend", version="1.0.0", lifespan=lifespan)
app.include_router(embeddings_router.router)
app.include_router(base_router)
app.include_router(articles_router, prefix="/articles", tags=["Articles"])
app.include_router(search_router.router)
app.include_router(cleanup_old_news_router)
app.include_router(cleanup_router)
app.include_router(news_analysis_router, prefix="/api")
