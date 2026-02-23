# URL Shortener API

A production-ready URL shortening service built with **FastAPI**, **PostgreSQL**, and **Docker**. Inspired by services like Bitly and TinyURL.

## Features

- Shorten any valid URL to a 7-character key
- Redirect with click tracking (302)
- Analytics endpoint per short URL
- Health check endpoint for cloud deployments
- Fully containerized with Docker Compose
- Test suite with SQLite (no external dependencies in CI)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.111 |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Containerization | Docker + Docker Compose |
| Testing | Pytest |

## Architecture

```
app/
├── main.py          # FastAPI app + startup
├── config.py        # Settings via pydantic-settings
├── database.py      # SQLAlchemy engine + session DI
├── models.py        # ORM models
├── schemas.py       # Pydantic request/response schemas
├── routers/
│   └── urls.py      # HTTP layer (routes only)
└── services/
    └── shortener.py # Business logic (pure functions)
```

## Getting Started

### Prerequisites
- Docker and Docker Compose installed

### Run locally

```bash
git clone https://github.com/YOUR_USERNAME/url-shortener
cd url-shortener

cp .env.example .env

docker-compose up --build
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

## API Reference

### `POST /shorten`
Shorten a URL.

**Request:**
```json
{ "original_url": "https://www.example.com/very/long/path" }
```

**Response (201):**
```json
{
  "key": "aB3xK9z",
  "short_url": "http://localhost:8000/aB3xK9z",
  "original_url": "https://www.example.com/very/long/path",
  "click_count": 0,
  "created_at": "2025-01-01T00:00:00Z"
}
```

### `GET /{key}`
Redirects to the original URL (302).

### `GET /{key}/stats`
Returns URL metadata and click count without redirecting.

### `GET /health`
Returns service health status.

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Engineering Decisions

**302 vs 301 redirect:** Using 302 (temporary) so browsers don't cache the redirect — every request hits the server, enabling accurate click tracking. 301 would be more performant but breaks analytics.

**Collision handling:** Keys are generated using `secrets.choice` (cryptographically secure). On collision, a new key is generated. At scale, a distributed ID generator (e.g., Snowflake) would be preferable.

**Sync click tracking:** Incremented synchronously for simplicity. In a high-traffic system, this should be offloaded to a message queue (Kafka, Redis Streams) to decouple analytics from the redirect hot path.
## Interface
<img width="1919" height="882" alt="image" src="https://github.com/user-attachments/assets/2e79a17c-af90-40b4-a9b1-6997daa27c4a" />
<img width="1919" height="874" alt="image" src="https://github.com/user-attachments/assets/b9c9a1f5-0047-4fe2-8157-cbdf816c64d4" />

## License

MIT
