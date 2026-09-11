"""Analysis endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.stock_service import StockService

router = APIRouter()


@router.get("/{symbol}/fundamentals")
async def get_fundamentals(symbol: str, db: Session = Depends(get_db)):
    """Get fundamental analysis"""
    try:
        fundamentals = await StockService.get_fundamentals(symbol, db)
        if not fundamentals:
            raise HTTPException(status_code=404, detail=f"No fundamentals found for {symbol}")
        return fundamentals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/technical")
async def get_technical(symbol: str, db: Session = Depends(get_db)):
    """Get technical analysis"""
    try:
        technical = await StockService.get_technical_analysis(symbol, db)
        if not technical:
            raise HTTPException(status_code=404, detail=f"No technical data found for {symbol}")
        return technical
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/sentiment")
async def get_sentiment(symbol: str, db: Session = Depends(get_db)):
    """Get news sentiment analysis"""
    try:
        sentiment = await StockService.get_sentiment(symbol, db)
        if not sentiment:
            raise HTTPException(status_code=404, detail=f"No sentiment data found for {symbol}")
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
