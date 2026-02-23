from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict


class URLCreate(BaseModel):
    """Request body for creating a short URL."""
    original_url: HttpUrl  # Pydantic validates URL format automatically


class URLResponse(BaseModel):
    """Response returned after shortening a URL."""
    key: str
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime

    # Pydantic v2: allows reading from ORM objects (SQLAlchemy models)
    model_config = ConfigDict(from_attributes=True)


class URLStats(URLResponse):
    """Extended response including analytics."""
    pass
