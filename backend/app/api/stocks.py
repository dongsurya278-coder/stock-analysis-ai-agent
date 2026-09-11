"""Stock data endpoints - FULLY IMPLEMENTED"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from loguru import logger
from ..database import get_db
from ..services.stock_service import StockService

router = APIRouter()
stock_service = StockService()


@router.get("/")
async def get_stocks(limit: int = Query(100, ge=1, le=200), db: Session = Depends(get_db)):
    """Get all monitored top stocks - IMPLEMENTED"""
    try:
        logger.info(f"Fetching top {limit} stocks")
        stocks = await stock_service.get_top_stocks(db, limit=limit)
        return {
            "status": "success",
            "data": stocks,
            "count": len(stocks)
        }
    except Exception as e:
        logger.error(f"Error getting stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
async def get_stock_detail(symbol: str, db: Session = Depends(get_db)):
    """Get detailed stock information - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching detail for {symbol}")
        
        stock = await stock_service.get_stock_detail(symbol, db)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        
        return {
            "status": "success",
            "data": stock
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stock detail for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history")
async def get_stock_history(symbol: str, days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """Get stock price history - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching {days}-day history for {symbol}")
        
        history = await stock_service.get_price_history(symbol, days, db)
        return {
            "status": "success",
            "symbol": symbol,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting price history for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update/{symbol}")
async def update_stock(symbol: str, db: Session = Depends(get_db)):
    """Manually update stock price - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Manually updating {symbol}")
        
        success = await stock_service.update_stock_price(symbol, db)
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to update {symbol}")
        
        return {
            "status": "success",
            "message": f"{symbol} updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
