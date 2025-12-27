from asyncio.log import logger
from app.models.news.news_article import NewsArticle
from app.models.news.ai_analysis import AiAnalysis
from app.services.search.search_service import search_similar_articles
import datetime
from app.services.deepseek_client.deepseek_client import analyze_article_with_deepseek
from app.database.database import SessionLocal


async def process_article(article_id: int):
    # ---- STEP 0: Load article (short-lived session)
    with SessionLocal() as db:
        article = db.query(NewsArticle).filter_by(id=article_id).first()
        if not article:
            return

        article_data = {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "content": article.content,
            "category": article.category,
        }

    # ---- STEP 1: Semantic search (READ-ONLY session)
    with SessionLocal() as db:
        references = await search_similar_articles(
            db,
            query_text=article_data["content"],
            category=article_data["category"],
            current_id=article_data["id"],
        )

    # ---- STEP 2: DeepSeek (NO DB session at all)
    output = await analyze_article_with_deepseek(
        article={
            "title": article_data["title"],
            "summary": article_data["summary"],
        },
        similar_articles=references,
    )

    logger.warning(f"[DeepSeek OUTPUT] -> {output}")
    logger.warning(f"[DeepSeek TYPE] -> {type(output)}")

    # ---- STEP 3: Persist analysis + mark analyzed (WRITE session)
    with SessionLocal() as db:
        try:
            prediction_text = (
                output.get("prediction", "")
                if isinstance(output, dict)
                else str(output)
            )

            analysis = AiAnalysis(
                article_id=article_data["id"],
                prediction=prediction_text,
                created_at=datetime.datetime.utcnow(),
            )

            db.add(analysis)

            article = db.query(NewsArticle).get(article_data["id"])
            article.is_analyzed = True

            db.commit()

            logger.info(f"✅ Article ID={article_data['id']} marked as analyzed")

        except Exception as e:
            db.rollback()
            logger.error(
                f"❌ Failed processing article ID={article_data['id']}: {e}",
                exc_info=True,
            )
