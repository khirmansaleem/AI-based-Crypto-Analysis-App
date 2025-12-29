import asyncio
from asyncio.log import logger
from app.models.news.news_article import NewsArticle
from app.models.news.ai_analysis import AiAnalysis
from app.services.search.search_service import search_similar_articles
import datetime
from app.services.deepseek_client.deepseek_client import analyze_article_with_deepseek
from app.database.database import SessionLocal


async def process_article(article_id: int):

    # STEP 0 — load article (OFF event loop)
    def load_article():
        with SessionLocal() as db:
            article = db.query(NewsArticle).filter_by(id=article_id).first()
            if not article:
                return None

            return {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "content": article.content,
                "category": article.category,
            }

    article_data = await asyncio.to_thread(load_article)
    if not article_data:
        return

    # STEP 1 — semantic search (OFF event loop)
    references = await asyncio.to_thread(
        search_similar_articles,  # ❌ no lambda, no async
        article_data["content"],
        article_data["category"],
        article_data["id"],
    )

    # STEP 2 — DeepSeek analysis (OFF event loop)
    output = await asyncio.to_thread(
        analyze_article_with_deepseek,  # ✅ already sync
        {
            "title": article_data["title"],
            "summary": article_data["summary"],
        },
        references,
    )

    # STEP 3 — persist analysis (OFF event loop)
    def persist():
        with SessionLocal() as db:
            analysis = AiAnalysis(
                article_id=article_data["id"],
                prediction=str(output),
                created_at=datetime.datetime.utcnow(),
            )
            db.add(analysis)

            article = db.query(NewsArticle).get(article_data["id"])
            article.is_analyzed = True
            db.commit()

    await asyncio.to_thread(persist)
