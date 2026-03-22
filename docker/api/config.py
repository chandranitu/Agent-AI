from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # PostgreSQL — uses Docker service name as host
    DB_HOST:     str = os.getenv("DB_HOST", "postgres")
    DB_PORT:     int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME:     str = os.getenv("DB_NAME", "test")
    DB_USER:     str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")

    # Ollama runs on HOST machine — special Docker DNS name
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    OLLAMA_MODEL:    str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    LLM_TEMPERATURE: float = 0.0

    # File storage — mapped to Docker volume
    UPLOAD_DIR: str = "/app/data/uploads"

    ALLOWED_EXTENSIONS: list = [
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".pdf", ".doc", ".docx",
        ".md", ".txt", ".csv",
        ".mp4", ".avi", ".mov",
        ".ppt", ".pptx",
        ".xlsx",
    ]
    MAX_FILE_SIZE_MB: int = 100

    class Config:
        env_file = ".env"

settings = Settings()
