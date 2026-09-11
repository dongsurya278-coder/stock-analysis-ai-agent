"""SQLAlchemy database models"""
from sqlalchemy import Column, String, Float, DateTime, Integer, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class Stock(Base):
    """Stock data model"""
    __tablename__ = "stocks"
    
    symbol = Column(String(10), primary_key=True, index=True)
    company_name = Column(String(255))
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StockPrice(Base):
    """Stock price history"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    price = Column(Float)
    change = Column(Float, nullable=True)
    change_percent = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class Fundamentals(Base):
    """Stock fundamentals"""
    __tablename__ = "fundamentals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    pe_ratio = Column(Float, nullable=True)
    peg_ratio = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)
    revenue = Column(Float, nullable=True)
    net_income = Column(Float, nullable=True)
    debt_to_equity = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    roa = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class TechnicalData(Base):
    """Technical indicators"""
    __tablename__ = "technical_data"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    rsi = Column(Float, nullable=True)
    macd = Column(Float, nullable=True)
    macd_signal = Column(Float, nullable=True)
    ma50 = Column(Float, nullable=True)
    ma200 = Column(Float, nullable=True)
    support = Column(Float, nullable=True)
    resistance = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class NewsSentiment(Base):
    """News and sentiment analysis"""
    __tablename__ = "news_sentiment"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String(20))  # positive, neutral, negative
    news_count = Column(Integer)
    summary = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class SignalEnum(str, enum.Enum):
    """Signal strength enum"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class BuySignal(Base):
    """AI-generated buy signals"""
    __tablename__ = "buy_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    confidence_score = Column(Float)  # 0 to 1
    signal_strength = Column(String(20))  # strong_buy, buy, hold, sell, strong_sell
    reasoning = Column(Text)
    entry_price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    fundamental_score = Column(Float)  # 0 to 100
    technical_score = Column(Float)  # 0 to 100
    sentiment_score = Column(Float)  # -100 to 100
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AnalysisLog(Base):
    """Log of AI agent analysis runs"""
    __tablename__ = "analysis_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    agent_response = Column(Text)
    execution_time = Column(Float)  # seconds
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
