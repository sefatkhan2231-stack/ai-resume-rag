from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- General ---
    APP_NAME: str = "AI Resume Screening API"
    FRONTEND_URL: str = "http://localhost:5173"

    # --- Storage ---
    UPLOAD_DIR: str = "./storage/uploads"
    VECTOR_DB_PATH: str = "./storage/chroma"
    DATABASE_PATH: str = "./storage/app.db"

    # --- LLM ---
    OLLAMA_MODEL: str = "llama3.2"

    # --- Optional keys, kept for future providers ---
    OPENAI_API_KEY: str | None = None
    HF_TOKEN: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
