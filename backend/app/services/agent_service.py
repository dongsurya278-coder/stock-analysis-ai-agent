"""AI Agent service for stock analysis"""
from loguru import logger
from typing import Optional
from ..models import BuySignal, AgentAnalysisResponse
from ..agents.stock_analyzer import StockAnalyzer


class AgentService:
    """Service for AI agent operations"""
    
    def __init__(self):
        self.analyzer = StockAnalyzer()
    
    async def analyze_stock(self, symbol: str, detailed: bool = False) -> AgentAnalysisResponse:
        """Run AI agent analysis on a stock"""
        try:
            logger.info(f"Starting AI analysis for {symbol}")
            result = await self.analyzer.analyze(symbol, detailed=detailed)
            logger.info(f"Completed AI analysis for {symbol}")
            return result
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            raise
    
    async def get_buy_signal(self, symbol: str) -> Optional[BuySignal]:
        """Get buy signal for stock"""
        try:
            signal = await self.analyzer.generate_signal(symbol)
            return signal
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            raise
