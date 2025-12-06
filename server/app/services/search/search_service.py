from typing import List, Tuple
from sqlalchemy import text, bindparam, Integer
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector

from app.services.ai.embeddings import get_embedding
from app.services.ai.summarizer import generate_summary


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
PRIMARY_THRESHOLD = 0.70  # strong similarity cutoff
FALLBACK_THRESHOLD = 0.60  # softer similarity if primary fails
MAX_FETCH = 20  # initial pool from pgvector
MAX_CONTEXT_RESULTS = 5  # final RAG references count
MAX_DAYS = 14  # recency filter
EMBED_DIM = 768  # mpnet embedding size


# ---------------------------------------------------------
# SQL TEMPLATE (Used for both primary + fallback)
# ---------------------------------------------------------
BASE_SQL = f"""
SELECT
    na.id,
    na.title,
    na.url,
    na.content,
    na.category,
    na.created_at,
    1 - (e.embedding <=> :query_embedding) AS similarity_score
FROM embeddings e
JOIN news_articles na ON na.id = e.article_id
WHERE na.created_at >= NOW() - INTERVAL '{MAX_DAYS} days'
ORDER BY e.embedding <=> :query_embedding
LIMIT :limit
"""


# ---------------------------------------------------------
# Helper: Execute pgvector query
# ---------------------------------------------------------
def _run_vector_query(db: Session, query_vector, limit: int):
    sql = text(BASE_SQL).bindparams(
        bindparam("query_embedding", type_=Vector(EMBED_DIM)),
        bindparam("limit", type_=Integer),
    )

    return (
        db.execute(
            sql,
            {"query_embedding": query_vector, "limit": limit},
        )
        .mappings()
        .all()
    )


# ---------------------------------------------------------
# Helper: Convert row into summary dict
# ---------------------------------------------------------
def _row_to_article_summary(row):
    summary = generate_summary(row["content"], max_sentences=4)

    return {
        "id": row["id"],
        "title": row["title"],
        "url": row["url"],
        "summary": f"{row['title']}. {summary}",
        "category": row["category"],
        "created_at": row["created_at"],
        "similarity": float(row["similarity_score"]),
    }


# ---------------------------------------------------------
# MAIN LOGIC: Semantic search with fallback
# ---------------------------------------------------------
def search_similar_articles(
    db: Session,
    query_text: str,
) -> List[Tuple[dict, float]]:

    # 1. Generate embedding
    query_vector = get_embedding(query_text)

    # 2. Run primary query (top 20)
    initial_rows = _run_vector_query(db, query_vector, MAX_FETCH)

    primary_results = []

    # 3. Filter using primary threshold
    for row in initial_rows:
        sim = float(row["similarity_score"])

        if sim >= PRIMARY_THRESHOLD:
            primary_results.append((_row_to_article_summary(row), sim))

    # 4. If we have good matches → return top 5
    if primary_results:
        primary_results.sort(key=lambda x: x[1], reverse=True)
        return primary_results[:MAX_CONTEXT_RESULTS]

    # ---------------------------------------------------------
    # FALLBACK LOGIC (No article ≥ 0.70)
    # ---------------------------------------------------------
    fallback_results = []

    for row in initial_rows:
        sim = float(row["similarity_score"])

        if sim >= FALLBACK_THRESHOLD:
            fallback_results.append((_row_to_article_summary(row), sim))

    # Sorted by similarity
    fallback_results.sort(key=lambda x: x[1], reverse=True)

    # If fallback threshold produced results
    if fallback_results:
        return fallback_results[:MAX_CONTEXT_RESULTS]

    # ---------------------------------------------------------
    # FINAL SAFETY NET: Return top 5 raw articles (no threshold)
    # DeepSeek performs better with some context than none.
    # ---------------------------------------------------------
    final_fallback = [
        (_row_to_article_summary(row), float(row["similarity_score"]))
        for row in initial_rows[:MAX_CONTEXT_RESULTS]
    ]

    return final_fallback
