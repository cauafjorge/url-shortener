import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use SQLite in-memory for tests — no Postgres required in CI
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_shorten_url():
    response = client.post("/shorten", json={"original_url": "https://www.google.com"})
    assert response.status_code == 201
    data = response.json()
    assert "key" in data
    assert "short_url" in data
    assert data["click_count"] == 0


def test_redirect():
    # Create a short URL first
    create_response = client.post("/shorten", json={"original_url": "https://www.github.com"})
    key = create_response.json()["key"]

    # Follow redirect
    response = client.get(f"/{key}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.github.com"


def test_click_tracking():
    create_response = client.post("/shorten", json={"original_url": "https://www.python.org"})
    key = create_response.json()["key"]

    # Hit the redirect 3 times
    for _ in range(3):
        client.get(f"/{key}", follow_redirects=False)

    stats_response = client.get(f"/{key}/stats")
    assert stats_response.json()["click_count"] == 3


def test_url_not_found():
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404


def test_invalid_url():
    response = client.post("/shorten", json={"original_url": "not-a-url"})
    assert response.status_code == 422  # Pydantic validation error
