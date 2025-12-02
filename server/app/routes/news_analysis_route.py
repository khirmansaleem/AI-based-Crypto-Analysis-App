from fastapi import APIRouter, HTTPException

from app.services.deepseek_client.deepseek_client import analyze_article_with_deepseek


router = APIRouter()


# ------------------------------------------------------------------
# PLACEHOLDER DB FUNCTIONS (Replace with real SQLAlchemy queries)
# ------------------------------------------------------------------
async def get_article_by_id(article_id: int):
    """
    Replace with your real database fetch.
    Must return: { "title": ..., "content": ... }
    """
    # Example placeholder
    return {
        "id": article_id,
        "title": "Bitcoin ETF Sees Record Inflow",
        "content": "BlackRock's Bitcoin ETF recorded the highest daily inflow...",
    }


async def get_similar_articles(article_id: int):
    """
    Replace with REAL pgvector semantic search.
    Must return list of dict: [{title:..., content:...}]
    """
    return [
        {
            "title": "Institutional Bitcoin demand rises",
            "content": "More institutions are increasing Bitcoin exposure...",
        },
        {
            "title": "ETF inflows correlate with BTC price rise",
            "content": "Historically, ETF inflows indicate bullish momentum...",
        },
    ]


# ------------------------------------------------------------------
# ROUTE: Analyze specific article & classify NO_IMPACT
# ------------------------------------------------------------------
@router.get("/analyze-news/{article_id}")
async def analyze_news(article_id: int):

    # 1. Fetch the article
    article = await get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # 2. Get similar articles (pgvector)
    similar = await get_similar_articles(article_id)

    # 3. Run full analysis (DeepSeek Reasoner)
    ai_response = await analyze_article_with_deepseek(article, similar)

    # 4. Check NO_IMPACT logic
    if ai_response.strip() == "NO_IMPACT":
        return {
            "article_id": article_id,
            "status": "NO_IMPACT",
            "save_to_db": False,
            "analysis": None,
        }

    # 5. Standard impactful news → YOU WILL SAVE THIS TO DATABASE
    return {
        "article_id": article_id,
        "status": "IMPACT",
        "save_to_db": True,
        "analysis": ai_response,
    }
