from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Insight360 AI"
    app_env: str = "local"
    app_port: int = 8000
    api_prefix: str = "/api"
    database_url: str = "******localhost:5432/insight360"
    readonly_database_url: str = "******localhost:5432/insight360"
    cors_origins: str = "http://localhost:5173"
    max_upload_size_mb: int = 15
    query_timeout_seconds: int = 15
    ai_provider: str = "deterministic"
    openai_base_url: str | None = None
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    ai_max_rows: int = 500

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
