"""Stock service with business logic"""
from sqlalchemy.orm import Session
from loguru import logger
from ..db.crud import StockCRUD, PriceCRUD, SignalCRUD


class StockService:
    """Service for stock operations"""
    
    @staticmethod
    async def get_top_stocks(db: Session, limit: int = 100):
        """Get top stocks to monitor"""
        try:
            stocks = StockCRUD.get_all_stocks(db, limit=limit)
            logger.info(f"Retrieved {len(stocks)} stocks")
            return stocks
        except Exception as e:
            logger.error(f"Error getting stocks: {e}")
            raise
    
    @staticmethod
    async def get_stock_detail(symbol: str, db: Session):
        """Get detailed stock information"""
        try:
            stock = StockCRUD.get_stock(db, symbol)
            if not stock:
                return None
            
            latest_price = PriceCRUD.get_latest_price(db, symbol)
            latest_signal = SignalCRUD.get_latest_signal(db, symbol)
            
            return {
                "symbol": symbol,
                "stock": stock,
                "price": latest_price,
                "signal": latest_signal,
            }
        except Exception as e:
            logger.error(f"Error getting stock detail for {symbol}: {e}")
            raise
    
    @staticmethod
    async def get_price_history(symbol: str, days: int, db: Session):
        """Get stock price history"""
        try:
            history = PriceCRUD.get_price_history(db, symbol, days)
            logger.info(f"Retrieved {len(history)} price points for {symbol}")
            return history
        except Exception as e:
            logger.error(f"Error getting price history for {symbol}: {e}")
            raise
    
    @staticmethod
    async def get_fundamentals(symbol: str, db: Session):
        """Get fundamental analysis"""
        # TODO: Implement fundamentals retrieval
        return None
    
    @staticmethod
    async def get_technical_analysis(symbol: str, db: Session):
        """Get technical analysis"""
        # TODO: Implement technical analysis
        return None
    
    @staticmethod
    async def get_sentiment(symbol: str, db: Session):
        """Get sentiment analysis"""
        # TODO: Implement sentiment analysis
        return None
