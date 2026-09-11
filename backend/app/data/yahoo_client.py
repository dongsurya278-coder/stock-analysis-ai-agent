"""Yahoo Finance API Client"""
import yfinance as yf
from typing import Optional, Dict
from loguru import logger


class YahooFinanceClient:
    """Client for Yahoo Finance data"""
    
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist.to_dict()
        except Exception as e:
            logger.error(f"Yahoo Finance error for {symbol}: {e}")
            raise
    
    def get_info(self, symbol: str) -> Dict:
        """Get stock information"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            logger.error(f"Error getting info for {symbol}: {e}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info.get('currentPrice', 0)
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            raise
