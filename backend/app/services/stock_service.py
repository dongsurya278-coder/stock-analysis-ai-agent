"""Stock service with business logic - FULLY IMPLEMENTED"""
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime
from typing import List, Optional
from ..db.crud import StockCRUD, PriceCRUD, SignalCRUD
from ..db.models import Stock, StockPrice, BuySignal
from ..data.iex_client import IEXCloudClient
from ..data.yahoo_client import YahooFinanceClient


class StockService:
    """Service for stock operations - Production Ready"""
    
    def __init__(self):
        self.iex_client = IEXCloudClient()
        self.yahoo_client = YahooFinanceClient()
    
    async def get_top_stocks(self, db: Session, limit: int = 100) -> list:
        """Get top stocks to monitor"""
        try:
            stocks = StockCRUD.get_all_stocks(db, limit=limit)
            logger.info(f"✅ Retrieved {len(stocks)} stocks")
            return stocks
        except Exception as e:
            logger.error(f"❌ Error getting stocks: {e}")
            raise
    
    async def get_stock_detail(self, symbol: str, db: Session) -> dict:
        """Get detailed stock information"""
        try:
            stock = StockCRUD.get_stock(db, symbol)
            if not stock:
                # Try to create new stock entry
                try:
                    company_info = self.iex_client.get_company_info(symbol)
                    stock = StockCRUD.create_stock(
                        db, symbol, 
                        company_info.get('companyName', symbol),
                        company_info.get('sector')
                    )
                except:
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
            logger.error(f"❌ Error getting stock detail for {symbol}: {e}")
            raise
    
    async def get_price_history(self, symbol: str, days: int, db: Session) -> list:
        """Get stock price history"""
        try:
            history = PriceCRUD.get_price_history(db, symbol, days)
            logger.info(f"✅ Retrieved {len(history)} price points for {symbol}")
            return history
        except Exception as e:
            logger.error(f"❌ Error getting price history for {symbol}: {e}")
            raise
    
    async def update_stock_price(self, symbol: str, db: Session) -> bool:
        """Update stock price from API"""
        try:
            quote = self.iex_client.get_quote(symbol)
            
            # Create price record
            PriceCRUD.create_price(
                db, symbol,
                quote.get('price', 0),
                quote.get('change', 0),
                quote.get('changePercent', 0),
                quote.get('volume', 0)
            )
            
            logger.info(f"✅ Updated price for {symbol}: ${quote.get('price', 0):.2f}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating price for {symbol}: {e}")
            return False
    
    async def initialize_top_stocks(self, db: Session, count: int = 100) -> int:
        """Initialize database with top stocks"""
        try:
            logger.info(f"📊 Initializing {count} top stocks...")
            
            # Get top gainers and losers
            gainers = self.iex_client.get_top_gainers()
            losers = self.iex_client.get_top_losers()
            
            symbols = set()
            for item in gainers + losers:
                symbols.add(item.get('symbol'))
            
            # Take top N
            symbols = list(symbols)[:count]
            
            created_count = 0
            for symbol in symbols:
                try:
                    existing = StockCRUD.get_stock(db, symbol)
                    if not existing:
                        company_info = self.iex_client.get_company_info(symbol)
                        StockCRUD.create_stock(
                            db, symbol,
                            company_info.get('companyName', symbol),
                            company_info.get('sector')
                        )
                        created_count += 1
                except Exception as e:
                    logger.warning(f"Could not create stock {symbol}: {e}")
            
            logger.info(f"✅ Initialized {created_count} new stocks")
            return created_count
        except Exception as e:
            logger.error(f"❌ Error initializing stocks: {e}")
            raise
