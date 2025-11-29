from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(Text, nullable=False)
    url = Column(Text, unique=True, nullable=False)
    content = Column(Text, nullable=False)

    category = Column(Text, nullable=False)
    published_at = Column(TIMESTAMP, nullable=True)
    hash = Column(Text, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_relevant = Column(Integer, default=1)

    embeddings = relationship(
        "Embedding",
        back_populates="article",
        cascade="all, delete",
        passive_deletes=True,
    )

    # ⭐ REQUIRED (fixes your crash)
    analysis = relationship(
        "AiAnalysis",
        back_populates="article",
        cascade="all, delete",
        passive_deletes=True,
    )
