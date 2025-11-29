# app/database/__init__.py

from app.models.news.news_article import NewsArticle
from app.models.news.embedding import Embedding
from app.models.news.ai_analysis import AiAnalysis  # if you have this

# Export models for Base.metadata
__all__ = ["NewsArticle", "Embedding", "AiAnalysis"]
