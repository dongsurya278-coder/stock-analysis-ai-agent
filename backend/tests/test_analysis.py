"""Tests for analysis modules"""
import pytest
from app.analysis.fundamentals import FundamentalAnalyzer
from app.analysis.technical import TechnicalAnalyzer
from app.analysis.sentiment import SentimentAnalyzer


def test_fundamental_analyzer():
    """Test fundamental analysis"""
    result = FundamentalAnalyzer.analyze_valuation(
        pe_ratio=25.0,
        peg_ratio=1.5,
        industry_avg_pe=20.0
    )
    assert result is not None


def test_technical_analyzer():
    """Test technical analysis"""
    prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 110, 112, 114, 113]
    rsi = TechnicalAnalyzer.calculate_rsi(prices)
    assert rsi is not None


@pytest.mark.asyncio
async def test_sentiment_analyzer():
    """Test sentiment analysis"""
    headlines = ["Stock surges on good earnings", "Company faces headwinds"]
    result = SentimentAnalyzer.analyze_headlines(headlines)
    assert result is not None
