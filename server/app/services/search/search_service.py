from typing import List, Tuple
from sqlalchemy import text, bindparam, Integer
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector

from app.services.ai.embeddings import get_embedding
from app.services.ai.summarizer import generate_summary


SIMILARITY_THRESHOLD = 0.55  # realistic for mpnet embeddings
MAX_CONTEXT_RESULTS = 5
MAX_DAYS = 14  # strict recency, but using created_at now


def search_similar_articles(
    db: Session,
    query_text: str,
    limit: int = 20,  # fetch more, filter after
) -> List[Tuple[dict, float]]:

    query_vector = get_embedding(query_text)

    sql = text(
        f"""
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
    ).bindparams(
        bindparam("query_embedding", type_=Vector(768)),
        bindparam("limit", type_=Integer),
    )

    rows = (
        db.execute(
            sql,
            {"query_embedding": query_vector, "limit": limit},
        )
        .mappings()
        .all()
    )

    results: List[Tuple[dict, float]] = []

    for row in rows:
        similarity = float(row["similarity_score"])

        # strict similarity filter
        if similarity < SIMILARITY_THRESHOLD:
            continue

        # summarizer: use sentence-based summarizer (v3)
        content_summary = generate_summary(row["content"], max_sentences=4)
        final_summary = f"{row['title']}. {content_summary}"

        article_dict = {
            "id": row["id"],
            "title": row["title"],
            "url": row["url"],
            "summary": final_summary,
            "category": row.get("category"),
            "created_at": row.get("created_at"),
            "similarity": similarity,
        }

        results.append((article_dict, similarity))

    # Sort by similarity (recency already filtered in SQL)
    results.sort(key=lambda x: x[1], reverse=True)

    # If nothing found → graceful fallback (give top 3 irrespective of threshold)
    if not results:
        fallback_sql = text(
            f"""
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
        ).bindparams(
            bindparam("query_embedding", type_=Vector(768)),
            bindparam("limit", type_=Integer),
        )

        fallback_rows = (
            db.execute(fallback_sql, {"query_embedding": query_vector}).mappings().all()
        )

        fallback_results = []
        for row in fallback_rows:
            content_summary = generate_summary(row["content"], max_sentences=4)
            article_dict = {
                "id": row["id"],
                "title": row["title"],
                "url": row["url"],
                "summary": f"{row['title']}. {content_summary}",
                "category": row["category"],
                "created_at": row["created_at"],
                "similarity": float(row["similarity_score"]),
            }
            fallback_results.append((article_dict, float(row["similarity_score"])))

        return fallback_results

    return results[:MAX_CONTEXT_RESULTS]
