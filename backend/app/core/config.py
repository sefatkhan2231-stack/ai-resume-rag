from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- General ---
    APP_NAME: str = "AI Resume Screening API"
    FRONTEND_URL: str = "https://ai-resume-rag-rho.vercel.app"

    # --- Storage ---
    UPLOAD_DIR: str = "./storage/uploads"
    VECTOR_DB_PATH: str = "./storage/chroma"
    DATABASE_PATH: str = "./storage/app.db"

    # --- LLM ---
    LLM_PROVIDER: str = "ollama"
    OLLAMA_MODEL: str = "llama3.2:1b"
    OLLAMA_HOST: str = "http://localhost:11434"


@lru_cache
def get_settings() -> Settings:
    return Settings()
