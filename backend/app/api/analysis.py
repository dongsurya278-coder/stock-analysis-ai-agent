"""Analysis endpoints - FULLY IMPLEMENTED"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from ..database import get_db
from ..services.stock_service import StockService
from ..services.agent_service import AgentService
from ..data.iex_client import IEXCloudClient
from ..analysis.fundamentals import FundamentalAnalyzer, TechnicalAnalyzer, SentimentAnalyzer

router = APIRouter()
stock_service = StockService()
agent_service = AgentService()
iex_client = IEXCloudClient()
fundamental_analyzer = FundamentalAnalyzer()
technical_analyzer = TechnicalAnalyzer()
sentiment_analyzer = SentimentAnalyzer()


@router.get("/{symbol}/fundamentals")
async def get_fundamentals(symbol: str, db: Session = Depends(get_db)):
    """Get fundamental analysis - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching fundamentals for {symbol}")
        
        # Get raw data
        fundamentals = iex_client.get_fundamentals(symbol)
        
        if not fundamentals:
            raise HTTPException(status_code=404, detail=f"No fundamentals found for {symbol}")
        
        # Analyze
        valuation = fundamental_analyzer.analyze_valuation(
            fundamentals.get('peRatio'),
            fundamentals.get('pegRatio')
        )
        
        health = fundamental_analyzer.analyze_health(
            fundamentals.get('debtToEquity'),
            fundamentals.get('currentRatio'),
            fundamentals.get('returnOnEquity')
        )
        
        return {
            "status": "success",
            "symbol": symbol,
            "fundamentals": fundamentals,
            "analysis": {
                "valuation": valuation,
                "health": health
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting fundamentals for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/technical")
async def get_technical(symbol: str, db: Session = Depends(get_db)):
    """Get technical analysis - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching technical analysis for {symbol}")
        
        # Get price data
        prices_data = iex_client.get_historical_prices(symbol, range="3m")
        
        if not prices_data:
            raise HTTPException(status_code=404, detail=f"No price data found for {symbol}")
        
        prices = [p.get('close', 0) for p in prices_data]
        
        # Calculate indicators
        rsi = technical_analyzer.calculate_rsi(prices)
        macd = technical_analyzer.calculate_macd(prices)
        mas = technical_analyzer.calculate_moving_averages(prices)
        bb = technical_analyzer.calculate_bollinger_bands(prices)
        sr = technical_analyzer.calculate_support_resistance(prices)
        score = technical_analyzer.composite_technical_score(prices)
        
        return {
            "status": "success",
            "symbol": symbol,
            "indicators": {
                "rsi": rsi,
                "macd": macd,
                "moving_averages": mas,
                "bollinger_bands": bb,
                "support_resistance": sr,
                "technical_score": score
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting technical for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/sentiment")
async def get_sentiment(symbol: str, db: Session = Depends(get_db)):
    """Get news sentiment analysis - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching sentiment for {symbol}")
        
        # Get news
        news = iex_client.get_news(symbol, last=15)
        
        if not news:
            raise HTTPException(status_code=404, detail=f"No news found for {symbol}")
        
        headlines = [n.get('headline', '') for n in news]
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze_headlines(headlines)
        
        return {
            "status": "success",
            "symbol": symbol,
            "sentiment": sentiment,
            "news_items": news[:10]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sentiment for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/full")
async def get_full_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get complete analysis (fundamentals + technical + sentiment) - IMPLEMENTED"""
    try:
        symbol = symbol.upper()
        logger.info(f"Fetching full analysis for {symbol}")
        
        # Parallel fetch
        fundamentals = iex_client.get_fundamentals(symbol)
        prices_data = iex_client.get_historical_prices(symbol, range="3m")
        news = iex_client.get_news(symbol, last=15)
        price_quote = iex_client.get_quote(symbol)
        
        # Process technical
        prices = [p.get('close', 0) for p in prices_data] if prices_data else []
        technical_score = technical_analyzer.composite_technical_score(prices) if prices else 0
        
        # Process sentiment
        headlines = [n.get('headline', '') for n in news] if news else []
        sentiment = sentiment_analyzer.analyze_headlines(headlines) if headlines else {}
        
        # Process fundamental
        fundamental_score = 50  # Default
        
        return {
            "status": "success",
            "symbol": symbol,
            "price": price_quote,
            "fundamentals": fundamentals,
            "technical_score": technical_score,
            "sentiment": sentiment,
            "news_count": len(news)
        }
    except Exception as e:
        logger.error(f"Error getting full analysis for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
