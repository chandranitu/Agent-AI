"""
config.py — Central configuration. Edit these values for your environment.
"""
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # ── PostgreSQL 18.1 ──────────────────────────────────────────────────────
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "test"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # ── Local file storage ───────────────────────────────────────────────────
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "..", "data", "uploads")
    ALLOWED_EXTENSIONS: list = [
        ".jpg", ".jpeg", ".png", ".gif", ".webp",   # images
        ".pdf", ".doc", ".docx",                    # documents
        ".md", ".txt",                              # text
        ".mp4", ".avi", ".mov",                     # video
        ".ppt", ".pptx",                            # presentations
        ".csv", ".xlsx",                            # spreadsheets
    ]
    MAX_FILE_SIZE_MB: int = 100

    # ── Local LLM (Ollama) ───────────────────────────────────────────────────
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    #OLLAMA_MODEL: str = "llama3"      # or mistral, phi3, gemma2, etc.
    OLLAMA_MODEL: str = "llama3.2:latest"
    LLM_TEMPERATURE: float = 0.0     # 0 = deterministic, minimal hallucination

    # ── App ──────────────────────────────────────────────────────────────────
    APP_SECRET: str = "change-me-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
