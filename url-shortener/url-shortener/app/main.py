from fastapi import FastAPI
from app.database import Base, engine
from app.routers import urls

# Create tables on startup (use Alembic migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A production-ready URL shortening service built with FastAPI and PostgreSQL.",
    version="1.0.0",
)

app.include_router(urls.router)


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Required by cloud platforms (AWS ECS, GCP Cloud Run, Railway, Render)
    to verify the service is alive before routing traffic.
    """
    return {"status": "healthy"}
