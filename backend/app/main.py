"""FastAPI application entry point"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from loguru import logger

from .config import get_settings
from .database import engine
from .db.models import Base
from .api import stocks, analysis, signals, websocket
from .scheduler import tasks

settings = get_settings()

# Configure logging
logger.add(
    "logs/app.log",
    rotation="500 MB",
    level=settings.agent_log_level,
)

logging.basicConfig(level=settings.agent_log_level)

# Initialize database
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Stock Analysis AI Agent starting up...")
    logger.info(f"Analyzing top {settings.top_stocks_count} stocks")
    logger.info(f"Update frequency: {settings.update_frequency_seconds}s")
    
    # Start background tasks
    tasks.start_scheduler()
    
    yield
    
    # Shutdown
    logger.info("🛑 Stock Analysis AI Agent shutting down...")
    tasks.stop_scheduler()


app = FastAPI(
    title="Stock Analysis AI Agent",
    description="Real-time AI-powered US stock analysis with fundamental, technical, and sentiment analysis",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Stock Analysis AI Agent API",
        "version": "0.1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "stock-analysis-ai-agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.fastapi_host,
        port=settings.fastapi_port,
    )
