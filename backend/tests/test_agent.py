"""Tests for AI agent"""
import pytest
from app.agents.stock_analyzer import StockAnalyzer


@pytest.mark.asyncio
async def test_stock_analyzer_init():
    """Test StockAnalyzer initialization"""
    analyzer = StockAnalyzer()
    assert analyzer is not None
    assert analyzer.model == "claude-3-5-sonnet-20241022"


@pytest.mark.asyncio
async def test_analyze_stock():
    """Test stock analysis"""
    # TODO: Implement with mocked data
    pass
