"""Database CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from . import models
from ..models import BuySignal as BuySignalSchema


class StockCRUD:
    """CRUD operations for stocks"""
    
    @staticmethod
    def get_stock(db: Session, symbol: str):
        return db.query(models.Stock).filter(models.Stock.symbol == symbol).first()
    
    @staticmethod
    def get_all_stocks(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Stock).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_stock(db: Session, symbol: str, company_name: str, sector: str = None):
        db_stock = models.Stock(symbol=symbol, company_name=company_name, sector=sector)
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock


class PriceCRUD:
    """CRUD operations for stock prices"""
    
    @staticmethod
    def create_price(db: Session, symbol: str, price: float, change: float = None, volume: int = None):
        db_price = models.StockPrice(
            symbol=symbol,
            price=price,
            change=change,
            volume=volume
        )
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price
    
    @staticmethod
    def get_latest_price(db: Session, symbol: str):
        return db.query(models.StockPrice).filter(
            models.StockPrice.symbol == symbol
        ).order_by(desc(models.StockPrice.timestamp)).first()
    
    @staticmethod
    def get_price_history(db: Session, symbol: str, days: int = 30):
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(models.StockPrice).filter(
            models.StockPrice.symbol == symbol,
            models.StockPrice.timestamp >= cutoff_date
        ).order_by(models.StockPrice.timestamp.desc()).all()


class SignalCRUD:
    """CRUD operations for buy signals"""
    
    @staticmethod
    def create_signal(db: Session, symbol: str, signal_data: dict):
        db_signal = models.BuySignal(
            symbol=symbol,
            **signal_data
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
        return db_signal
    
    @staticmethod
    def get_latest_signal(db: Session, symbol: str):
        return db.query(models.BuySignal).filter(
            models.BuySignal.symbol == symbol
        ).order_by(desc(models.BuySignal.created_at)).first()
    
    @staticmethod
    def get_active_signals(db: Session, limit: int = 100):
        return db.query(models.BuySignal).filter(
            models.BuySignal.is_active == True
        ).order_by(desc(models.BuySignal.confidence_score)).limit(limit).all()
    
    @staticmethod
    def get_strong_buy_signals(db: Session):
        return db.query(models.BuySignal).filter(
            models.BuySignal.is_active == True,
            models.BuySignal.signal_strength == "strong_buy"
        ).order_by(desc(models.BuySignal.confidence_score)).all()
