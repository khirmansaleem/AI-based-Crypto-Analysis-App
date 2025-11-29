from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.database import get_db

router = APIRouter()


@router.get("/ping")
def ping():
    return {"status": "ok", "message": "FastAPI backend is running"}


@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT NOW();")).fetchone()
    return {"db_time": str(result[0])}
