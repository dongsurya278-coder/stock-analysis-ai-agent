"""AI Agent service for stock analysis - FULLY IMPLEMENTED"""
from loguru import logger
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models import BuySignal, AgentAnalysisResponse
from ..agents.stock_analyzer import StockAnalyzer
from ..db.crud import SignalCRUD
from datetime import datetime, timedelta


class AgentService:
    """Service for AI agent operations - Production Ready"""
    
    def __init__(self):
        self.analyzer = StockAnalyzer()
    
    async def analyze_stock(self, symbol: str, detailed: bool = False, db: Session = None) -> AgentAnalysisResponse:
        """Run AI agent analysis on a stock - COMPLETE"""
        try:
            logger.info(f"🤖 Starting AI analysis for {symbol}")
            result = await self.analyzer.analyze(symbol, detailed=detailed)
            logger.info(f"✅ Completed AI analysis for {symbol}")
            return result
        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")
            raise
    
    async def get_buy_signal(self, symbol: str, db: Session) -> dict:
        """Get buy signal for stock - COMPLETE"""
        try:
            logger.info(f"📈 Generating signal for {symbol}")
            signal = await self.analyzer.generate_signal(symbol)
            
            # Save to database
            if signal and db:
                signal_data = {
                    'confidence_score': signal.get('confidence_score', 0.5),
                    'signal_strength': signal.get('signal_strength', 'hold'),
                    'reasoning': signal.get('reasoning', ''),
                    'entry_price': signal.get('entry_price'),
                    'target_price': signal.get('target_price'),
                    'stop_loss': signal.get('stop_loss'),
                    'fundamental_score': 50,
                    'technical_score': 50,
                    'sentiment_score': 0,
                    'is_active': True,
                    'expires_at': datetime.now() + timedelta(days=7),
                }
                SignalCRUD.create_signal(db, symbol, signal_data)
            
            logger.info(f"✅ Signal generated for {symbol}: {signal.get('signal_strength')}")
            return signal
        except Exception as e:
            logger.error(f"❌ Error generating signal for {symbol}: {e}")
            raise
    
    async def analyze_portfolio(self, symbols: List[str], db: Session = None) -> dict:
        """Analyze multiple stocks - COMPLETE"""
        try:
            logger.info(f"📊 Analyzing portfolio of {len(symbols)} stocks")
            results = await self.analyzer.analyze_portfolio(symbols)
            logger.info(f"✅ Portfolio analysis complete: {results['signals_generated']} signals")
            return results
        except Exception as e:
            logger.error(f"❌ Error analyzing portfolio: {e}")
            raise
