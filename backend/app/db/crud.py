"""Database CRUD operations - FULLY IMPLEMENTED"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from .models import Stock, StockPrice, BuySignal


class StockCRUD:
    """CRUD operations for stocks - IMPLEMENTED"""
    
    @staticmethod
    def create_stock(db: Session, symbol: str, name: str, sector: str = None):
        stock = Stock(symbol=symbol, name=name, sector=sector)
        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock
    
    @staticmethod
    def get_stock(db: Session, symbol: str):
        return db.query(Stock).filter(Stock.symbol == symbol).first()
    
    @staticmethod
    def get_all_stocks(db: Session, limit: int = 100):
        return db.query(Stock).limit(limit).all()
    
    @staticmethod
    def update_stock(db: Session, symbol: str, **kwargs):
        stock = StockCRUD.get_stock(db, symbol)
        if stock:
            for key, value in kwargs.items():
                setattr(stock, key, value)
            db.commit()
            db.refresh(stock)
        return stock


class PriceCRUD:
    """CRUD operations for prices - IMPLEMENTED"""
    
    @staticmethod
    def create_price(db: Session, symbol: str, price: float, change: float = 0, 
                    change_percent: float = 0, volume: int = 0):
        price_record = StockPrice(
            symbol=symbol,
            price=price,
            change=change,
            change_percent=change_percent,
            volume=volume
        )
        db.add(price_record)
        db.commit()
        db.refresh(price_record)
        return price_record
    
    @staticmethod
    def get_latest_price(db: Session, symbol: str):
        return db.query(StockPrice).filter(
            StockPrice.symbol == symbol
        ).order_by(desc(StockPrice.timestamp)).first()
    
    @staticmethod
    def get_price_history(db: Session, symbol: str, days: int = 30):
        since = datetime.utcnow() - timedelta(days=days)
        return db.query(StockPrice).filter(
            StockPrice.symbol == symbol,
            StockPrice.timestamp >= since
        ).order_by(StockPrice.timestamp).all()


class SignalCRUD:
    """CRUD operations for signals - IMPLEMENTED"""
    
    @staticmethod
    def create_signal(db: Session, symbol: str, signal_data: dict):
        signal = BuySignal(symbol=symbol, **signal_data)
        db.add(signal)
        db.commit()
        db.refresh(signal)
        return signal
    
    @staticmethod
    def get_latest_signal(db: Session, symbol: str):
        return db.query(BuySignal).filter(
            BuySignal.symbol == symbol
        ).order_by(desc(BuySignal.created_at)).first()
    
    @staticmethod
    def get_active_signals(db: Session, limit: int = 100):
        now = datetime.utcnow()
        return db.query(BuySignal).filter(
            BuySignal.is_active == True,
            BuySignal.expires_at > now
        ).order_by(desc(BuySignal.confidence_score)).limit(limit).all()
    
    @staticmethod
    def get_strong_buy_signals(db: Session):
        now = datetime.utcnow()
        return db.query(BuySignal).filter(
            BuySignal.signal_strength.in_(['strong_buy', 'buy']),
            BuySignal.is_active == True,
            BuySignal.expires_at > now
        ).order_by(desc(BuySignal.confidence_score)).all()
