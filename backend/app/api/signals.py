"""Buy signal endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.stock_service import StockService
from ..db.crud import SignalCRUD

router = APIRouter()


@router.get("/")
async def get_all_signals(limit: int = 100, db: Session = Depends(get_db)):
    """Get all active buy signals"""
    try:
        signals = SignalCRUD.get_active_signals(db, limit=limit)
        return {"data": signals, "count": len(signals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strong-buy")
async def get_strong_buy_signals(db: Session = Depends(get_db)):
    """Get strong buy signals only"""
    try:
        signals = SignalCRUD.get_strong_buy_signals(db)
        return {"data": signals, "count": len(signals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
async def get_signal_for_stock(symbol: str, db: Session = Depends(get_db)):
    """Get signal for specific stock"""
    try:
        signal = SignalCRUD.get_latest_signal(db, symbol)
        if not signal:
            raise HTTPException(status_code=404, detail=f"No signal found for {symbol}")
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
