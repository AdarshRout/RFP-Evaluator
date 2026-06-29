from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    groq_max_tokens: int = 4096
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    hf_token: str | None = None
    chunk_size: int = 600
    chunk_overlap: int = 100
    retrieval_top_k: int = 4
    rfp_chunk_size: int = 6000
    rfp_chunk_overlap: int = 500
    cors_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]
    app_env: str = "production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
