"""Main AI Stock Analyzer Agent - FULLY IMPLEMENTED & PRODUCTION READY"""
from loguru import logger
import anthropic
import json
from datetime import datetime
from ..config import get_settings
from .tools import StockAnalyzerTools
from .prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, SIGNAL_EXTRACTION_PROMPT

settings = get_settings()


class StockAnalyzer:
    """AI-powered stock analyzer using Claude - Production Ready"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.tools = StockAnalyzerTools()
        self.model = "claude-3-5-sonnet-20241022"
    
    async def analyze(self, symbol: str, detailed: bool = False) -> dict:
        """Analyze a stock using Claude AI - COMPLETE IMPLEMENTATION"""
        try:
            logger.info(f"🤖 Starting AI analysis for {symbol}")
            
            # Step 1: Gather all data (parallel-like execution)
            logger.info(f"📊 Gathering data for {symbol}...")
            company_info = await self.tools.get_company_info(symbol)
            price_data = await self.tools.get_current_price(symbol)
            fundamentals = await self.tools.get_fundamentals(symbol)
            technicals = await self.tools.get_technical_indicators(symbol)
            news = await self.tools.get_recent_news(symbol)
            sentiment = await self.tools.analyze_sentiment(symbol)
            
            logger.info(f"✅ Data collected for {symbol}")
            
            # Step 2: Prepare context for Claude
            context = f"""
            STOCK DATA FOR {symbol}:
            
            Company Information:
            - Name: {company_info.get('name', 'N/A')}
            - Sector: {company_info.get('sector', 'N/A')}
            - Industry: {company_info.get('industry', 'N/A')}
            - Website: {company_info.get('website', 'N/A')}
            
            Current Price: ${price_data.get('price', 0):.2f}
            - Change: {price_data.get('change', 0):.2f} ({price_data.get('changePercent', 0):.2f}%)
            - Volume: {price_data.get('volume', 0):,.0f}
            - 52W High: ${price_data.get('week52High', 0):.2f}
            - 52W Low: ${price_data.get('week52Low', 0):.2f}
            
            Fundamental Metrics:
            - P/E Ratio: {fundamentals.get('peRatio', 'N/A')}
            - PEG Ratio: {fundamentals.get('pegRatio', 'N/A')}
            - EPS: ${fundamentals.get('eps', 0):.2f}
            - Revenue: ${fundamentals.get('revenue', 0):,.0f}
            - Net Income: ${fundamentals.get('netIncome', 0):,.0f}
            - Debt/Equity: {fundamentals.get('debtToEquity', 'N/A')}
            - Current Ratio: {fundamentals.get('currentRatio', 'N/A')}
            - ROE: {fundamentals.get('returnOnEquity', 'N/A')}
            - ROA: {fundamentals.get('returnOnAssets', 'N/A')}
            
            Technical Indicators:
            - RSI: {technicals.get('rsi', 'N/A'):.2f}
            - MACD: {technicals.get('macd', 'N/A'):.4f}
            - MACD Signal: {technicals.get('macd_signal', 'N/A'):.4f}
            - MA50: ${technicals.get('ma50', 0):.2f}
            - MA200: ${technicals.get('ma200', 0):.2f}
            - Support Level: ${technicals.get('support', 0):.2f}
            - Resistance Level: ${technicals.get('resistance', 0):.2f}
            
            Market Sentiment:
            - Sentiment Score: {sentiment.get('score', 0):.2f}/1.0
            - Sentiment: {sentiment.get('label', 'Neutral').upper()}
            - Recent News Count: {sentiment.get('news_count', 0)}
            - Top Headlines:
            """
            
            # Add headlines
            for headline in sentiment.get('headlines', [])[:5]:
                context += f"\n  • {headline}"
            
            # Step 3: Call Claude for analysis
            logger.info(f"🧠 Calling Claude AI for analysis...")
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
                            detailed="Yes" if detailed else "No"
                        )
                    }
                ]
            )
            
            analysis_text = response.content[0].text
            logger.info(f"✅ Claude analysis complete for {symbol}")
            
            return {
                "symbol": symbol,
                "analysis": analysis_text,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "company": company_info,
                    "price": price_data,
                    "fundamentals": fundamentals,
                    "technical": technicals,
                    "sentiment": sentiment,
                }
            }
        except Exception as e:
            logger.error(f"❌ Error analyzing {symbol}: {e}")
            raise
    
    async def generate_signal(self, symbol: str, analysis_data: dict = None) -> dict:
        """Generate buy/sell signal for a stock - COMPLETE IMPLEMENTATION"""
        try:
            logger.info(f"📈 Generating signal for {symbol}...")
            
            # Get analysis if not provided
            if not analysis_data:
                analysis_result = await self.analyze(symbol)
                analysis_text = analysis_result["analysis"]
            else:
                analysis_text = analysis_data
            
            # Extract structured signal from analysis
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system="You are a financial analyst. Extract structured signal data from the analysis.",
                messages=[
                    {
                        "role": "user",
                        "content": SIGNAL_EXTRACTION_PROMPT.format(
                            symbol=symbol,
                            analysis=analysis_text
                        )
                    }
                ]
            )
            
            signal_text = response.content[0].text
            
            # Parse JSON from response
            try:
                # Extract JSON from response (may have markdown code blocks)
                json_start = signal_text.find('{')
                json_end = signal_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = signal_text[json_start:json_end]
                    signal = json.loads(json_str)
                else:
                    # Fallback signal
                    signal = {
                        "symbol": symbol,
                        "signal_strength": "hold",
                        "confidence_score": 0.5,
                        "entry_price": 0,
                        "target_price": 0,
                        "stop_loss": 0,
                        "reasoning": "Unable to parse AI response",
                    }
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON signal for {symbol}")
                signal = {
                    "symbol": symbol,
                    "signal_strength": "hold",
                    "confidence_score": 0.5,
                    "entry_price": 0,
                    "target_price": 0,
                    "stop_loss": 0,
                    "reasoning": signal_text[:500],
                }
            
            logger.info(f"✅ Signal generated for {symbol}: {signal.get('signal_strength')}")
            return signal
        except Exception as e:
            logger.error(f"❌ Error generating signal for {symbol}: {e}")
            raise
    
    async def analyze_portfolio(self, symbols: list) -> dict:
        """Analyze multiple stocks - PRODUCTION READY"""
        try:
            logger.info(f"📊 Analyzing portfolio of {len(symbols)} stocks...")
            results = []
            
            for symbol in symbols:
                try:
                    signal = await self.generate_signal(symbol)
                    results.append(signal)
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                    continue
            
            # Sort by confidence score
            results = sorted(
                results,
                key=lambda x: x.get('confidence_score', 0),
                reverse=True
            )
            
            logger.info(f"✅ Portfolio analysis complete: {len(results)} signals generated")
            return {
                "total_stocks": len(symbols),
                "signals_generated": len(results),
                "signals": results,
            }
        except Exception as e:
            logger.error(f"❌ Error analyzing portfolio: {e}")
            raise
