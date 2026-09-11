"""Pydantic models for API requests/responses"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class StockPrice(BaseModel):
    """Stock price data"""
    symbol: str
    price: float
    currency: str = "USD"
    timestamp: datetime
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[int] = None


class Fundamentals(BaseModel):
    """Stock fundamental metrics"""
    symbol: str
    pe_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    earnings_per_share: Optional[float] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity
    roa: Optional[float] = None  # Return on Assets
    growth_rate: Optional[float] = None
    market_cap: Optional[float] = None


class TechnicalIndicators(BaseModel):
    """Technical analysis indicators"""
    symbol: str
    rsi: Optional[float] = None  # Relative Strength Index
    macd: Optional[float] = None  # MACD value
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    moving_average_50: Optional[float] = None
    moving_average_200: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None


class NewsSentiment(BaseModel):
    """News sentiment analysis"""
    symbol: str
    sentiment_score: float = Field(..., ge=-1, le=1)  # -1 to 1
    sentiment_label: str  # positive, neutral, negative
    recent_news_count: int
    headlines: List[str] = []
    summary: Optional[str] = None


class BuySignal(BaseModel):
    """AI-generated buy signal"""
    symbol: str
    confidence_score: float = Field(..., ge=0, le=1)  # 0 to 1
    signal_strength: str  # strong_buy, buy, hold, sell, strong_sell
    reasoning: str
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    fundamental_score: float = Field(..., ge=0, le=100)
    technical_score: float = Field(..., ge=0, le=100)
    sentiment_score: float = Field(..., ge=-100, le=100)
    timestamp: datetime
    expires_at: Optional[datetime] = None


class StockAnalysis(BaseModel):
    """Complete stock analysis"""
    symbol: str
    company_name: Optional[str] = None
    price: StockPrice
    fundamentals: Fundamentals
    technical: TechnicalIndicators
    sentiment: NewsSentiment
    signal: Optional[BuySignal] = None
    updated_at: datetime


class AgentAnalysisRequest(BaseModel):
    """Request for AI agent analysis"""
    symbol: str
    detailed: bool = False


class AgentAnalysisResponse(BaseModel):
    """Response from AI agent"""
    symbol: str
    analysis: str
    buy_signal: Optional[BuySignal] = None
    reasoning: str
    alternatives: Optional[List[str]] = None
    risks: Optional[List[str]] = None


class PortfolioMetrics(BaseModel):
    """Portfolio level metrics"""
    total_stocks_analyzed: int
    buy_signals_count: int
    strong_buy_count: int
    neutral_count: int
    sell_signals_count: int
    average_confidence: float
    last_updated: datetime
