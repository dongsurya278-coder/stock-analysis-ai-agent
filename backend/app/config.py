"""Application Configuration"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API Keys
    iex_cloud_api_key: str
    anthropic_api_key: str
    
    # Database
    database_url: str = "sqlite:///./stock_agent.db"
    
    # Server
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    
    # Agent Settings
    agent_log_level: str = "INFO"
    research_batch_size: int = 100
    update_frequency_seconds: int = 60
    
    # Stock Settings
    top_stocks_count: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
