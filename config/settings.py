from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    REDIS_URL: str = "redis://localhost:6379/0"
    DUCKDB_DATABASE_PATH: str = "cube4disco.duckdb"
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
