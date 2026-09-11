"""Yahoo Finance API Client - IMPLEMENTED"""
import yfinance as yf
from typing import Optional, Dict, List
from loguru import logger
import pandas as pd


class YahooFinanceClient:
    """Client for Yahoo Finance data - Production Ready"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol: str, period: str = "3mo", interval: str = "1d") -> List[Dict]:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            data = []
            for date, row in hist.iterrows():
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']),
                })
            
            logger.info(f"Retrieved {len(data)} data points for {symbol}")
            return data
        except Exception as e:
            logger.error(f"Error getting stock data for {symbol}: {e}")
            return []
    
    def get_info(self, symbol: str) -> Dict:
        """Get stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'longName': info.get('longName'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'marketCap': info.get('marketCap'),
                'trailingPE': info.get('trailingPE'),
                'forwardPE': info.get('forwardPE'),
                'dividend': info.get('dividend'),
                'dividendYield': info.get('dividendYield'),
                'beta': info.get('beta'),
                '52WeekHigh': info.get('fiftyTwoWeekHigh'),
                '52WeekLow': info.get('fiftyTwoWeekLow'),
            }
        except Exception as e:
            logger.error(f"Error getting info for {symbol}: {e}")
            return {}
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.info.get('currentPrice', 0)
            logger.info(f"Got price for {symbol}: ${price}")
            return float(price) if price else 0
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return 0
    
    def get_earnings(self, symbol: str) -> Dict:
        """Get earnings information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'trailingEps': info.get('trailingEps'),
                'forwardEps': info.get('forwardEps'),
                'earningsGrowth': info.get('earningsGrowth'),
            }
        except Exception as e:
            logger.error(f"Error getting earnings for {symbol}: {e}")
            return {}
