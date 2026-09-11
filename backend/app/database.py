"""Database connection - FULLY IMPLEMENTED"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings
from loguru import logger

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

logger.info(f"Database configured: {settings.database_url}")


def get_db():
    """Get database session - IMPLEMENTED"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
