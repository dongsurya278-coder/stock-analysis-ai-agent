"""Main AI Stock Analyzer Agent using Claude"""
from loguru import logger
import anthropic
from ..config import get_settings
from .tools import StockAnalyzerTools
from .prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT

settings = get_settings()


class StockAnalyzer:
    """AI-powered stock analyzer using Claude"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.tools = StockAnalyzerTools()
        self.model = "claude-3-5-sonnet-20241022"
    
    async def analyze(self, symbol: str, detailed: bool = False) -> dict:
        """Analyze a stock using Claude AI"""
        try:
            logger.info(f"Analyzing {symbol} with Claude...")
            
            # Gather data
            company_info = await self.tools.get_company_info(symbol)
            price_data = await self.tools.get_current_price(symbol)
            fundamentals = await self.tools.get_fundamentals(symbol)
            technicals = await self.tools.get_technical_indicators(symbol)
            news = await self.tools.get_recent_news(symbol)
            sentiment = await self.tools.analyze_sentiment(symbol)
            
            # Prepare context
            context = f"""
            Stock Symbol: {symbol}
            Company: {company_info}
            Current Price: ${price_data}
            Fundamentals: {fundamentals}
            Technical Indicators: {technicals}
            Recent News: {news}
            News Sentiment: {sentiment}
            """
            
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": ANALYSIS_PROMPT.format(
                            symbol=symbol,
                            context=context,
                            detailed=detailed
                        )
                    }
                ]
            )
            
            analysis_text = response.content[0].text
            logger.info(f"Analysis complete for {symbol}")
            
            return {
                "symbol": symbol,
                "analysis": analysis_text,
                "context": context,
            }
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {e}")
            raise
    
    async def generate_signal(self, symbol: str) -> dict:
        """Generate buy/sell signal for a stock"""
        try:
            logger.info(f"Generating signal for {symbol}...")
            analysis = await self.analyze(symbol, detailed=True)
            
            # Parse signal from analysis
            # TODO: Extract structured signal from Claude response
            
            return {
                "symbol": symbol,
                "signal": "hold",
                "confidence": 0.5,
            }
        except Exception as e:
            logger.error(f"Error generating signal for {symbol}: {e}")
            raise
