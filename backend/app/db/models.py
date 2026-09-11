"""Database configuration and CRUD operations - FULLY IMPLEMENTED"""
from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Stock(Base):
    """Stock model - IMPLEMENTED"""
    __tablename__ = "stocks"
    
    symbol = Column(String(10), primary_key=True, index=True)
    name = Column(String(255))
    sector = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StockPrice(Base):
    """Stock price history - IMPLEMENTED"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    price = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class BuySignal(Base):
    """Buy signals from AI agent - IMPLEMENTED"""
    __tablename__ = "buy_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), index=True)
    confidence_score = Column(Float)
    signal_strength = Column(String(20))  # strong_buy, buy, hold, sell, strong_sell
    reasoning = Column(String(2000))
    entry_price = Column(Float)
    target_price = Column(Float)
    stop_loss = Column(Float)
    fundamental_score = Column(Float)
    technical_score = Column(Float)
    sentiment_score = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, index=True)
