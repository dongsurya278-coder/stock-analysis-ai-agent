"""IEX Cloud API Client"""
from typing import Optional, List, Dict
import requests
from loguru import logger
from ..config import get_settings

settings = get_settings()


class IEXCloudClient:
    """Client for IEX Cloud API"""
    
    BASE_URL = "https://cloud.iexapis.com/stable"
    
    def __init__(self):
        self.api_key = settings.iex_cloud_api_key
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request"""
        try:
            if params is None:
                params = {}
            params['token'] = self.api_key
            
            url = f"{self.BASE_URL}{endpoint}"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"IEX API error: {e}")
            raise
    
    def get_quote(self, symbol: str) -> Dict:
        """Get stock quote"""
        return self._make_request(f"/stock/{symbol}/quote")
    
    def get_fundamentals(self, symbol: str) -> Dict:
        """Get company fundamentals"""
        return self._make_request(f"/stock/{symbol}/stats")
    
    def get_company_info(self, symbol: str) -> Dict:
        """Get company information"""
        return self._make_request(f"/stock/{symbol}/company")
    
    def get_news(self, symbol: str, last: int = 10) -> List[Dict]:
        """Get latest news"""
        return self._make_request(f"/stock/{symbol}/news/last/{last}")
    
    def get_top_gainers(self) -> List[Dict]:
        """Get top gaining stocks"""
        return self._make_request("/stock/market/list/gainers")
    
    def get_top_losers(self) -> List[Dict]:
        """Get top losing stocks"""
        return self._make_request("/stock/market/list/losers")
