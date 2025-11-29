from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database.base import Base
from datetime import datetime


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("news_articles.id", ondelete="CASCADE"))
    embedding = Column(Vector(768), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    article = relationship("NewsArticle", back_populates="embeddings")
