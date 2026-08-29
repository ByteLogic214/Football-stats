from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    THESTATSAPI_KEY: str = ""
    THESTATSAPI_BASE_URL: str = "https://api.thestatsapi.com/api"
    APP_NAME: str = "Football Stats Analyzer"
    APP_VERSION: str = "1.0.0"
    CORS_ORIGINS: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
