from asyncio.log import logger
from app.models.news.news_article import NewsArticle
from app.models.news.ai_analysis import AiAnalysis
from app.services.search.search_service import search_similar_articles
import datetime
from app.services.deepseek_client.deepseek_client import analyze_article_with_deepseek


async def process_article(db, article_id: int):
    article = db.query(NewsArticle).filter_by(id=article_id).first()

    if not article:
        return

    # STEP 1 — Get references using semantic search
    references = await search_similar_articles(
        db,
        query_text=article.content,
        category=article.category,
        current_id=article.id,
    )

    # STEP 2 — DeepSeek analysis (RAW)
    output = await analyze_article_with_deepseek(
        article={
            "title": article.title,
            "summary": article.summary,
        },
        similar_articles=references,
    )

    logger.warning(f"[DeepSeek OUTPUT] -> {output}")
    logger.warning(f"[DeepSeek TYPE] -> {type(output)}")

    # STEP 3 — Persist RAW prediction (always)
    prediction_text = ""

    if isinstance(output, dict):
        prediction_text = output.get("prediction", "")
    elif isinstance(output, str):
        prediction_text = output
    else:
        prediction_text = str(output)

    analysis = AiAnalysis(
        article_id=article.id,
        prediction=prediction_text,
        created_at=datetime.datetime.utcnow(),
    )

    db.add(analysis)
    logger.info(f"💾 Saved RAW analysis for article ID={article.id}")

    # STEP 4 — Mark article as processed
    article.is_analyzed = True
    db.commit()

    logger.info(f"✅ Article ID={article.id} marked as analyzed")
