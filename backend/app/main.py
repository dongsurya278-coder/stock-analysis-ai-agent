"""Main FastAPI application - PRODUCTION READY"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys
from .api import stocks, analysis, signals, websocket
from .scheduler.tasks import start_scheduler, stop_scheduler
from .database import Base, engine
from .config import get_settings

# Configure logging
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/app.log", rotation="500 MB", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🤖 Stock Analysis AI Agent",
    description="AI-powered stock analysis with Claude AI, real-time data, and buy/sell signals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Initialize on startup - IMPLEMENTED"""
    logger.info("🚀 Starting Stock Analysis AI Agent...")
    logger.info(f"📊 Environment: {settings.environment}")
    logger.info(f"🗄️  Database: {settings.database_url}")
    logger.info(f"🤖 AI Model: Claude 3.5 Sonnet")
    
    # Start background scheduler
    start_scheduler()
    logger.info("✅ Application started successfully!")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown - IMPLEMENTED"""
    logger.info("⛔ Shutting down...")
    stop_scheduler()
    logger.info("✅ Application stopped")


# Register routers
app.include_router(
    stocks.router,
    prefix="/api/stocks",
    tags=["Stocks"]
)

app.include_router(
    analysis.router,
    prefix="/api/analysis",
    tags=["Analysis"]
)

app.include_router(
    signals.router,
    prefix="/api/signals",
    tags=["Signals"]
)

app.include_router(
    websocket.router,
    prefix="/ws",
    tags=["WebSocket"]
)


@app.get("/")
async def root():
    """Root endpoint - IMPLEMENTED"""
    return {
        "status": "success",
        "message": "🤖 Stock Analysis AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "api_docs": "/docs",
            "stocks": "/api/stocks",
            "analysis": "/api/analysis",
            "signals": "/api/signals",
            "websocket": "/ws/signals"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - IMPLEMENTED"""
    return {
        "status": "healthy",
        "service": "Stock Analysis AI Agent",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
