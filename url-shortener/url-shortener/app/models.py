from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func
from app.database import Base


class URL(Base):
    """
    Database model for shortened URLs.
    
    Design decisions:
    - `key` is indexed for fast lookups on redirect (the hot path)
    - `click_count` tracked server-side (requires 302, not 301)
    - `created_at` uses server-side default for consistency across timezones
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(10), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
