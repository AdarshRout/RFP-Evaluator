from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    groq_api_key: str
    # llama-3.1-8b-instant: 500K TPD 
    groq_model: str = "llama-3.1-8b-instant"
    # Scoring/extraction responses are short JSON - 1024 is plenty, saves ~75% tokens vs 4096
    groq_max_tokens: int = 1024
    groq_report_max_tokens: int = 2048 
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    hf_token: str | None = None
    chunk_size: int = 600
    chunk_overlap: int = 100
    # Fetch 3 chunks per requirement instead of 4 - reduces scorer prompt size
    retrieval_top_k: int = 3
    # Smaller RFP chunks → fewer requirements extracted → fewer LLM calls
    rfp_chunk_size: int = 4000
    rfp_chunk_overlap: int = 300
    # Hard cap: never extract more than 20 requirements to avoid TPD blowout
    max_requirements: int = 20
    cors_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]
    app_env: str = "production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
