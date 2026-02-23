from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import URLCreate, URLResponse, URLStats
from app.services.shortener import (
    create_short_url,
    get_url_by_key,
    increment_click,
    build_short_url,
)

router = APIRouter()


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    """
    Shorten a URL.
    
    - Validates URL format via Pydantic (HttpUrl)
    - Returns 201 Created with the short URL and metadata
    """
    url_entry = create_short_url(db, original_url=str(payload.original_url))
    return URLResponse(
        key=url_entry.key,
        short_url=build_short_url(url_entry.key),
        original_url=url_entry.original_url,
        click_count=url_entry.click_count,
        created_at=url_entry.created_at,
    )


@router.get("/{key}/stats", response_model=URLStats)
def get_url_stats(key: str, db: Session = Depends(get_db)):
    """
    Return analytics for a shortened URL without triggering a redirect.
    Note: route must be declared BEFORE /{key} to avoid conflict.
    """
    url_entry = get_url_by_key(db, key)
    if not url_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    return URLStats(
        key=url_entry.key,
        short_url=build_short_url(url_entry.key),
        original_url=url_entry.original_url,
        click_count=url_entry.click_count,
        created_at=url_entry.created_at,
    )


@router.get("/{key}")
def redirect_to_url(key: str, db: Session = Depends(get_db)):
    """
    Redirect to original URL.
    
    Uses 302 (temporary redirect) intentionally:
    - Browser won't cache the redirect
    - Every request hits our server → we can track clicks accurately
    - 301 would cache in browser and break analytics
    """
    url_entry = get_url_by_key(db, key)
    if not url_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    increment_click(db, url_entry)
    return RedirectResponse(url=url_entry.original_url, status_code=status.HTTP_302_FOUND)
