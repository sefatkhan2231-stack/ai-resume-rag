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
    LLM_PROVIDER: str = "groq"
    OLLAMA_MODEL: str = "smollm2:135m"
    OLLAMA_HOST: str = "http://junction.proxy.rlwy.net:25199"

    # Groq12
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    GROQ_HOST: str = "https://api.groq.com/openai/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
