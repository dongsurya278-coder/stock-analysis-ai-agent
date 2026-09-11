"""Background tasks and scheduler - FULLY IMPLEMENTED"""
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from datetime import datetime
import asyncio
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.stock_service import StockService
from ..services.agent_service import AgentService
from ..db.crud import StockCRUD

scheduler = BackgroundScheduler()
stock_service = StockService()
agent_service = AgentService()


def update_stock_data():
    """Scheduled task to update stock data every minute - IMPLEMENTED"""
    try:
        db = SessionLocal()
        logger.info(f"⏰ [{datetime.now()}] Starting stock data update...")
        
        # Get all stocks
        stocks = StockCRUD.get_all_stocks(db, limit=100)
        
        if not stocks:
            logger.warning("No stocks found. Initializing...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(stock_service.initialize_top_stocks(db))
            stocks = StockCRUD.get_all_stocks(db, limit=100)
        
        # Update prices
        updated = 0
        for stock in stocks:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(
                    stock_service.update_stock_price(stock.symbol, db)
                )
                if success:
                    updated += 1
            except Exception as e:
                logger.error(f"Error updating {stock.symbol}: {e}")
                continue
        
        logger.info(f"✅ Stock data update complete. Updated {updated}/{len(stocks)} stocks")
        db.close()
    except Exception as e:
        logger.error(f"❌ Error in stock data update: {e}")


def run_agent_analysis():
    """Scheduled task to run AI agent analysis every 5 minutes - IMPLEMENTED"""
    try:
        db = SessionLocal()
        logger.info(f"⏰ [{datetime.now()}] Starting AI agent analysis...")
        
        # Get top stocks with recent prices
        stocks = StockCRUD.get_all_stocks(db, limit=20)  # Analyze top 20 stocks
        
        if not stocks:
            logger.warning("No stocks to analyze")
            db.close()
            return
        
        symbols = [stock.symbol for stock in stocks]
        
        # Run analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(
            agent_service.analyze_portfolio(symbols, db)
        )
        
        logger.info(f"✅ AI agent analysis complete. Generated {results.get('signals_generated', 0)} signals")
        db.close()
    except Exception as e:
        logger.error(f"❌ Error in agent analysis: {e}")


def start_scheduler():
    """Start background scheduler - PRODUCTION READY"""
    logger.info("🚀 Starting background scheduler...")
    
    # Update stock data every 60 seconds
    scheduler.add_job(
        update_stock_data,
        'interval',
        seconds=60,
        id='update_stocks',
        name='Update Stock Data',
        max_instances=1,
        coalesce=True
    )
    
    # Run AI analysis every 5 minutes
    scheduler.add_job(
        run_agent_analysis,
        'interval',
        minutes=5,
        id='run_analysis',
        name='Run AI Agent Analysis',
        max_instances=1,
        coalesce=True
    )
    
    scheduler.start()
    logger.info("✅ Scheduler started with 2 background jobs")


def stop_scheduler():
    """Stop background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("✅ Scheduler stopped")
