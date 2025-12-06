from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.search.search_service import search_similar_articles


router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str


@router.post("/")
def semantic_search(body: SearchRequest, db: Session = Depends(get_db)):
    results = search_similar_articles(db, body.query)
    return {"query": body.query, "results": results}
