from functools import lru_cache
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import get_settings


@lru_cache
def get_llm(temperature: float = 0.0, max_tokens: int | None = None) -> ChatGroq:
    s = get_settings()
    return ChatGroq(
        model=s.groq_model,
        temperature=temperature,
        groq_api_key=s.groq_api_key,
        max_tokens=max_tokens if max_tokens is not None else s.groq_max_tokens,
    )


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    s = get_settings()
    kwargs = {
        "model_name": s.embedding_model,
        "model_kwargs": {"device": "cpu"},
        "encode_kwargs": {"normalize_embeddings": True},
    }
    if s.hf_token:
        kwargs["model_kwargs"]["token"] = s.hf_token
    return HuggingFaceEmbeddings(**kwargs)
