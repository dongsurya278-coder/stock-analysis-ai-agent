"""Stock data endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import StockPrice
from ..services.stock_service import StockService

router = APIRouter()


@router.get("/")
async def get_stocks(db: Session = Depends(get_db)):
    """Get all monitored stocks"""
    try:
        stocks = await StockService.get_top_stocks(db)
        return {"data": stocks, "count": len(stocks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
async def get_stock_detail(symbol: str, db: Session = Depends(get_db)):
    """Get detailed stock information"""
    try:
        stock = await StockService.get_stock_detail(symbol, db)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/history")
async def get_stock_history(symbol: str, days: int = 30, db: Session = Depends(get_db)):
    """Get stock price history"""
    try:
        history = await StockService.get_price_history(symbol, days, db)
        return {"symbol": symbol, "data": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
