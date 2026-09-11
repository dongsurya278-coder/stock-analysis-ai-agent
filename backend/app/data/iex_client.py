"""IEX Cloud API Client - IMPLEMENTED"""
from typing import Optional, List, Dict
import requests
from loguru import logger
from ..config import get_settings
import time

settings = get_settings()


class IEXCloudClient:
    """Client for IEX Cloud API - Production Ready"""
    
    BASE_URL = "https://cloud.iexapis.com/stable"
    
    def __init__(self):
        self.api_key = settings.iex_cloud_api_key
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Rate limiting
    
    def _rate_limit(self):
        """Implement rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with error handling"""
        try:
            self._rate_limit()
            
            if params is None:
                params = {}
            params['token'] = self.api_key
            
            url = f"{self.BASE_URL}{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            logger.info(f"IEX API success: {endpoint}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"IEX API error for {endpoint}: {e}")
            raise
    
    def get_quote(self, symbol: str) -> Dict:
        """Get stock quote - Price, change, volume"""
        try:
            data = self._make_request(f"/stock/{symbol}/quote")
            return {
                'symbol': symbol,
                'price': data.get('latestPrice', 0),
                'change': data.get('change', 0),
                'changePercent': data.get('changePercent', 0),
                'volume': data.get('latestVolume', 0),
                'timestamp': data.get('latestTime'),
                'marketCap': data.get('marketCap'),
                'peRatio': data.get('peRatio'),
                'week52High': data.get('week52High'),
                'week52Low': data.get('week52Low'),
            }
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {e}")
            raise
    
    def get_fundamentals(self, symbol: str) -> Dict:
        """Get company fundamentals"""
        try:
            data = self._make_request(f"/stock/{symbol}/stats")
            return {
                'symbol': symbol,
                'peRatio': data.get('peRatio'),
                'pegRatio': data.get('pegRatio'),
                'eps': data.get('latestEPS'),
                'revenue': data.get('revenue'),
                'netIncome': data.get('netIncome'),
                'debtToEquity': data.get('debtToEquity'),
                'currentRatio': data.get('currentRatio'),
                'returnOnEquity': data.get('returnOnEquity'),
                'returnOnAssets': data.get('returnOnAssets'),
                'profitMargin': data.get('profitMargin'),
            }
        except Exception as e:
            logger.error(f"Error getting fundamentals for {symbol}: {e}")
            raise
    
    def get_company_info(self, symbol: str) -> Dict:
        """Get company information"""
        try:
            data = self._make_request(f"/stock/{symbol}/company")
            return {
                'symbol': symbol,
                'companyName': data.get('companyName'),
                'industry': data.get('industry'),
                'sector': data.get('sector'),
                'description': data.get('description'),
                'website': data.get('website'),
                'employees': data.get('employees'),
                'ceo': data.get('CEO'),
            }
        except Exception as e:
            logger.error(f"Error getting company info for {symbol}: {e}")
            raise
    
    def get_news(self, symbol: str, last: int = 10) -> List[Dict]:
        """Get latest news for stock"""
        try:
            data = self._make_request(f"/stock/{symbol}/news/last/{last}")
            news_list = []
            for item in data:
                news_list.append({
                    'headline': item.get('headline'),
                    'summary': item.get('summary'),
                    'source': item.get('source'),
                    'url': item.get('url'),
                    'datetime': item.get('datetime'),
                    'image': item.get('image'),
                })
            return news_list
        except Exception as e:
            logger.error(f"Error getting news for {symbol}: {e}")
            return []
    
    def get_historical_prices(self, symbol: str, range: str = "3m") -> List[Dict]:
        """Get historical price data"""
        try:
            data = self._make_request(f"/stock/{symbol}/chart/{range}")
            prices = []
            for item in data:
                prices.append({
                    'date': item.get('date'),
                    'open': item.get('open'),
                    'close': item.get('close'),
                    'high': item.get('high'),
                    'low': item.get('low'),
                    'volume': item.get('volume'),
                })
            return prices
        except Exception as e:
            logger.error(f"Error getting historical prices for {symbol}: {e}")
            return []
    
    def get_top_gainers(self) -> List[Dict]:
        """Get top gaining stocks"""
        try:
            data = self._make_request("/stock/market/list/gainers")
            return data[:20] if data else []
        except Exception as e:
            logger.error(f"Error getting top gainers: {e}")
            return []
    
    def get_top_losers(self) -> List[Dict]:
        """Get top losing stocks"""
        try:
            data = self._make_request("/stock/market/list/losers")
            return data[:20] if data else []
        except Exception as e:
            logger.error(f"Error getting top losers: {e}")
            return []
