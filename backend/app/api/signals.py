"""Buy signal endpoints - FULLY IMPLEMENTED"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger
from ..database import get_db
from ..services.agent_service import AgentService
from ..db.crud import SignalCRUD

router = APIRouter()
agent_service = AgentService()


@router.get("/")
async def get_all_signals(limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    """Get all active buy signals - IMPLEMENTED"""
    try:
        logger.info(f"Fetching {limit} signals")
        signals = SignalCRUD.get_active_signals(db, limit=limit)
        
        return {
            "status": "success",
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strong-buy")
async def get_strong_buy_signals(db: Session = Depends(get_db)):
    """Get strong buy signals only - IMPLEMENTED"""
    try:
        logger.info("Fetching strong buy signals")
        signals = SignalCRUD.get_strong_buy_signals(db)
        
        return {
            "status": "success",
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"Error getting strong buy signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
async def get_signal_for_stock(symbol: str, db: Session = Depends(get_db)):
    """Get signal for specific stock - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching signal for {symbol}")
        
        signal = SignalCRUD.get_latest_signal(db, symbol)
        if not signal:
            raise HTTPException(status_code=404, detail=f"No signal found for {symbol}")
        
        return {
            "status": "success",
            "data": signal
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting signal for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/{symbol}")
async def generate_signal(symbol: str, db: Session = Depends(get_db)):
    """Manually generate signal for stock - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Generating signal for {symbol}")
        
        signal = await agent_service.get_buy_signal(symbol, db)
        
        return {
            "status": "success",
            "data": signal
        }
    except Exception as e:
        logger.error(f"Error generating signal for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def get_signals_summary(db: Session = Depends(get_db)):
    """Get summary statistics of all signals - IMPLEMENTED"""
    try:
        logger.info("Fetching signals summary")
        signals = SignalCRUD.get_active_signals(db, limit=10000)
        
        summary = {
            "total_signals": len(signals),
            "strong_buy": len([s for s in signals if s.signal_strength == "strong_buy"]),
            "buy": len([s for s in signals if s.signal_strength == "buy"]),
            "hold": len([s for s in signals if s.signal_strength == "hold"]),
            "sell": len([s for s in signals if s.signal_strength == "sell"]),
            "strong_sell": len([s for s in signals if s.signal_strength == "strong_sell"]),
        }
        
        if signals:
            summary["avg_confidence"] = sum(s.confidence_score for s in signals) / len(signals)
        
        return {
            "status": "success",
            "data": summary
        }
    except Exception as e:
        logger.error(f"Error getting signals summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
