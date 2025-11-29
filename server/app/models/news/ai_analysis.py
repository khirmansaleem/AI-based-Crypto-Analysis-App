from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime


class AiAnalysis(Base):
    __tablename__ = "ai_analysis"

    id = Column(Integer, primary_key=True, index=True)

    article_id = Column(Integer, ForeignKey("news_articles.id", ondelete="CASCADE"))
    prediction = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    article = relationship("NewsArticle", back_populates="analysis")
