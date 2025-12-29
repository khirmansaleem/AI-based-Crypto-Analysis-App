from typing import List
from app.services.ai.embeddings import get_embedding
from app.services.deepseek_client.summarizer import generate_summary
from sqlalchemy import text, bindparam, Integer
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector

from app.database.database import SessionLocal

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

PRIMARY_THRESHOLD = 0.70  # strong similarity cutoff
FALLBACK_THRESHOLD = 0.60  # softer similarity if primary fails
MAX_FETCH = 20  # initial pool from pgvector
MAX_CONTEXT_RESULTS = 5  # final RAG references count
EMBED_DIM = 768  # mpnet embedding size

# Dynamic recency windows based on category
CATEGORY_RECENCY_DAYS = {
    "regulation": 45,
    "etf": 14,
    "macro": 30,
    "exchanges": 14,
    "investments": 30,
    "stablecoins": 14,
}

DEFAULT_RECENCY = 21  # fallback if unknown category


# ---------------------------------------------------------
# SQL TEMPLATE (dynamic recency + exclude current article)
# ---------------------------------------------------------

BASE_SQL = """
SELECT
    na.id,
    na.title,
    na.url,
    na.content,
    na.category,
    na.published_at,
    1 - (e.embedding <=> :query_embedding) AS similarity_score
FROM embeddings e
JOIN news_articles na ON na.id = e.article_id
WHERE na.published_at >= NOW() - (INTERVAL '1 day' * :max_days)
  AND na.id != :current_id
ORDER BY e.embedding <=> :query_embedding
LIMIT :limit
"""


# ---------------------------------------------------------
# Helper: Execute pgvector query
# ---------------------------------------------------------


def _run_vector_query(
    db: Session, query_vector, max_days: int, limit: int, current_id: int
):
    sql = BASE_SQL.replace(":max_days", str(max_days))

    sql = text(sql).bindparams(
        bindparam("query_embedding", type_=Vector(EMBED_DIM)),
        bindparam("limit", type_=Integer),
        bindparam("current_id", type_=Integer),
    )

    return (
        db.execute(
            sql,
            {
                "query_embedding": query_vector,
                "limit": limit,
                "current_id": current_id,
            },
        )
        .mappings()
        .all()
    )


# ---------------------------------------------------------
# Helper: Convert row to dictionary used for RAG
# ---------------------------------------------------------


def _row_to_article_summary(row):
    """Convert a DB row into a clean summary reference object."""
    content_summary = generate_summary(
        row["content"],
        published_at=row["published_at"],
    )

    return {
        "id": row["id"],
        "title": row["title"],
        "summary": f"{row['title']}. {content_summary}",
        "url": row["url"],
        "category": row["category"],
        "published_at": row["published_at"],
        "similarity": float(row["similarity_score"]),
    }


# ---------------------------------------------------------
# MAIN LOGIC: Semantic search with dynamic recency windows
# ---------------------------------------------------------


def search_similar_articles(
    query_text: str, category: str, current_id: int
) -> List[dict]:

    max_days = CATEGORY_RECENCY_DAYS.get(category, DEFAULT_RECENCY)
    query_vector = get_embedding(query_text)

    with SessionLocal() as db:
        initial_rows = _run_vector_query(
            db, query_vector, max_days, MAX_FETCH, current_id
        )

    primary = []
    fallback = []

    for row in initial_rows:
        sim = float(row["similarity_score"])
        if sim >= PRIMARY_THRESHOLD:
            primary.append(row)
        elif sim >= FALLBACK_THRESHOLD:
            fallback.append(row)

    if primary:
        return [_row_to_article_summary(r) for r in primary[:MAX_CONTEXT_RESULTS]]

    if fallback:
        return [_row_to_article_summary(r) for r in fallback[:MAX_CONTEXT_RESULTS]]

    return [_row_to_article_summary(r) for r in initial_rows[:MAX_CONTEXT_RESULTS]]


# ---------------------------------------------------------
# END OF FILE
# ---------------------------------------------------------
