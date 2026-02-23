from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# SQLAlchemy engine — connection pool is handled automatically
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency injection for database sessions.
    FastAPI calls this on every request and closes the session after response.
    This is the standard pattern used in production FastAPI apps.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
