# Multi-stage build: keeps final image lean (no build tools in production)
FROM python:3.12-slim AS base

WORKDIR /app

# Install dependencies first (Docker layer caching — only re-runs if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
