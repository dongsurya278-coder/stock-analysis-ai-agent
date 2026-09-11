"""Tools for the AI Agent - FULLY IMPLEMENTED"""
from loguru import logger
from typing import Optional, List, Dict
import asyncio
from ..data.iex_client import IEXCloudClient
from ..data.yahoo_client import YahooFinanceClient
from ..analysis.fundamentals import FundamentalAnalyzer, TechnicalAnalyzer, SentimentAnalyzer


class StockAnalyzerTools:
    """Collection of tools for stock analysis - Production Ready"""
    
    def __init__(self):
        self.iex_client = IEXCloudClient()
        self.yahoo_client = YahooFinanceClient()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    async def get_company_info(self, symbol: str) -> dict:
        """Get company information - IMPLEMENTED"""
        try:
            logger.info(f"Fetching company info for {symbol}")
            iex_data = self.iex_client.get_company_info(symbol)
            yahoo_data = self.yahoo_client.get_info(symbol)
            
            return {
                'symbol': symbol,
                'name': iex_data.get('companyName', yahoo_data.get('longName', 'N/A')),
                'sector': iex_data.get('sector', yahoo_data.get('sector', 'N/A')),
                'industry': iex_data.get('industry', yahoo_data.get('industry', 'N/A')),
                'website': iex_data.get('website', 'N/A'),
                'description': iex_data.get('description', 'N/A'),
                'employees': iex_data.get('employees', 0),
            }
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            return {'symbol': symbol, 'name': symbol}
    
    async def get_current_price(self, symbol: str) -> dict:
        """Get current stock price - IMPLEMENTED"""
        try:
            logger.info(f"Fetching current price for {symbol}")
            quote = self.iex_client.get_quote(symbol)
            return quote
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return {'symbol': symbol, 'price': 0}
    
    async def get_fundamentals(self, symbol: str) -> dict:
        """Get fundamental metrics - IMPLEMENTED"""
        try:
            logger.info(f"Fetching fundamentals for {symbol}")
            iex_fundamentals = self.iex_client.get_fundamentals(symbol)
            yahoo_earnings = self.yahoo_client.get_earnings(symbol)
            
            # Analyze fundamentals
            valuation = self.fundamental_analyzer.analyze_valuation(
                iex_fundamentals.get('peRatio'),
                iex_fundamentals.get('pegRatio')
            )
            
            growth = self.fundamental_analyzer.analyze_growth(
                yahoo_earnings.get('earningsGrowth'),
                yahoo_earnings.get('forwardEps')
            )
            
            health = self.fundamental_analyzer.analyze_health(
                iex_fundamentals.get('debtToEquity'),
                iex_fundamentals.get('currentRatio'),
                iex_fundamentals.get('returnOnEquity')
            )
            
            composite_score = self.fundamental_analyzer.composite_fundamental_score(
                valuation, growth, health
            )
            
            return {
                'symbol': symbol,
                'peRatio': iex_fundamentals.get('peRatio'),
                'pegRatio': iex_fundamentals.get('pegRatio'),
                'eps': iex_fundamentals.get('eps'),
                'revenue': iex_fundamentals.get('revenue'),
                'netIncome': iex_fundamentals.get('netIncome'),
                'debtToEquity': iex_fundamentals.get('debtToEquity'),
                'currentRatio': iex_fundamentals.get('currentRatio'),
                'returnOnEquity': iex_fundamentals.get('returnOnEquity'),
                'returnOnAssets': iex_fundamentals.get('returnOnAssets'),
                'valuation': valuation,
                'growth': growth,
                'health': health,
                'composite_score': composite_score,
            }
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {symbol}: {e}")
            return {'symbol': symbol}
    
    async def get_technical_indicators(self, symbol: str) -> dict:
        """Get technical indicators - IMPLEMENTED"""
        try:
            logger.info(f"Fetching technical indicators for {symbol}")
            
            # Get historical price data
            prices_data = self.iex_client.get_historical_prices(symbol, range="3m")
            if not prices_data:
                prices_data = self.yahoo_client.get_stock_data(symbol, period="3mo")
            
            prices = [p.get('close', 0) for p in prices_data]
            
            if not prices:
                logger.warning(f"No price data available for {symbol}")
                return {'symbol': symbol}
            
            # Calculate technical indicators
            rsi = self.technical_analyzer.calculate_rsi(prices)
            macd = self.technical_analyzer.calculate_macd(prices)
            mas = self.technical_analyzer.calculate_moving_averages(prices)
            bb = self.technical_analyzer.calculate_bollinger_bands(prices)
            sr = self.technical_analyzer.calculate_support_resistance(prices)
            technical_score = self.technical_analyzer.composite_technical_score(prices)
            
            return {
                'symbol': symbol,
                'rsi': rsi,
                'macd': macd['macd'],
                'macd_signal': macd['signal'],
                'macd_histogram': macd['histogram'],
                'ma20': mas['ma20'],
                'ma50': mas['ma50'],
                'ma200': mas['ma200'],
                'bb_upper': bb['upper'],
                'bb_middle': bb['middle'],
                'bb_lower': bb['lower'],
                'support': sr['support'],
                'resistance': sr['resistance'],
                'technical_score': technical_score,
            }
        except Exception as e:
            logger.error(f"Error fetching technical indicators for {symbol}: {e}")
            return {'symbol': symbol}
    
    async def get_recent_news(self, symbol: str) -> list:
        """Get recent news headlines - IMPLEMENTED"""
        try:
            logger.info(f"Fetching news for {symbol}")
            news = self.iex_client.get_news(symbol, last=15)
            return [
                {
                    'headline': n.get('headline'),
                    'summary': n.get('summary'),
                    'source': n.get('source'),
                    'url': n.get('url'),
                    'datetime': n.get('datetime'),
                } for n in news
            ]
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []
    
    async def analyze_sentiment(self, symbol: str) -> dict:
        """Analyze sentiment from news - IMPLEMENTED"""
        try:
            logger.info(f"Analyzing sentiment for {symbol}")
            
            # Get news
            news = await self.get_recent_news(symbol)
            headlines = [n.get('headline', '') for n in news]
            
            # Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze_headlines(headlines)
            
            return {
                'symbol': symbol,
                'score': sentiment['sentiment_score'],
                'label': sentiment['sentiment_label'],
                'positive_count': sentiment['positive_count'],
                'negative_count': sentiment['negative_count'],
                'neutral_count': sentiment['neutral_count'],
                'news_count': sentiment['total_headlines'],
                'headlines': headlines[:5],
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {symbol}: {e}")
            return {'symbol': symbol, 'score': 0, 'label': 'neutral'}
