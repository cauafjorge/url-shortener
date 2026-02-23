from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/urlshortener"
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


# Singleton — imported across the app
settings = Settings()
