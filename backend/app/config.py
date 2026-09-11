"""Configuration settings - FULLY IMPLEMENTED"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings - Production Ready"""
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./stock_analysis.db"
    )
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    secret_key: str = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    
    # API Keys
    iex_cloud_api_key: str = os.getenv("IEX_CLOUD_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
