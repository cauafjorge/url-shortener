import secrets
import string
from sqlalchemy.orm import Session
from app.models import URL
from app.config import settings

# Characters used in the short key — URL-safe alphabet
ALPHABET = string.ascii_letters + string.digits
KEY_LENGTH = 7  # 62^7 = ~3.5 trillion combinations before collision


def generate_key() -> str:
    """
    Generate a cryptographically secure random key.
    
    Why secrets over random?
    - `random` is not cryptographically secure (predictable with enough samples)
    - `secrets` uses OS-level entropy, safe for security-sensitive tokens
    - This matters: predictable keys could allow enumeration attacks
    """
    return "".join(secrets.choice(ALPHABET) for _ in range(KEY_LENGTH))


def create_short_url(db: Session, original_url: str) -> URL:
    """
    Persist a new shortened URL to the database.
    
    Collision handling: regenerate key if it already exists.
    At scale, a smarter approach would use a distributed ID generator
    (e.g., Twitter Snowflake), but for this scope, retry is acceptable.
    """
    key = generate_key()

    # Retry on collision — extremely rare but must be handled
    while db.query(URL).filter(URL.key == key).first():
        key = generate_key()

    url_entry = URL(key=key, original_url=original_url)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)
    return url_entry


def get_url_by_key(db: Session, key: str) -> URL | None:
    """Fetch a URL entry by its short key."""
    return db.query(URL).filter(URL.key == key).first()


def increment_click(db: Session, url: URL) -> None:
    """
    Increment click counter.
    
    Trade-off: doing this synchronously adds latency to the redirect.
    At scale, you'd push this to a message queue (Kafka/Redis Streams)
    and process asynchronously — decoupling analytics from the hot path.
    """
    url.click_count += 1
    db.commit()


def build_short_url(key: str) -> str:
    return f"{settings.BASE_URL}/{key}"
