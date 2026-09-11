"""Prompts for Claude AI Agent"""

SYSTEM_PROMPT = """
You are an expert financial analyst and investment advisor with deep knowledge of:
- Fundamental analysis (P/E ratios, EPS, Revenue growth, Debt ratios, etc.)
- Technical analysis (Moving averages, RSI, MACD, Support/Resistance levels)
- Market sentiment and news analysis
- Risk assessment and portfolio management

Your task is to provide comprehensive stock analysis and actionable investment signals.
Always consider:
1. Company fundamentals and growth prospects
2. Technical setup and price action
3. Market sentiment and recent news
4. Risk/reward ratios
5. Entry and exit points

Provide clear reasoning for your conclusions and always mention key risks.
"""

ANALYSIS_PROMPT = """
Please analyze the following stock for investment opportunity:

Stock: {symbol}

Context:
{context}

Detailed Analysis: {detailed}

Provide:
1. Executive Summary (2-3 sentences)
2. Fundamental Analysis (strength/weakness)
3. Technical Analysis (current setup)
4. Sentiment Analysis (market sentiment)
5. Buy Signal Assessment (BUY/HOLD/SELL with confidence 0-100)
6. Entry Price Recommendation
7. Target Price (6-12 month outlook)
8. Stop Loss Level
9. Key Risks
10. Key Catalysts

Format your response as structured JSON at the end.
"""

BUY_SIGNAL_PROMPT = """
Based on the following analysis, generate a buy/sell signal:

{analysis}

Respond with a JSON object containing:
{{
    "symbol": "{symbol}",
    "signal_strength": "strong_buy|buy|hold|sell|strong_sell",
    "confidence_score": 0.0-1.0,
    "entry_price": number,
    "target_price": number,
    "stop_loss": number,
    "reasoning": "string",
    "risk_factors": ["string"],
    "positive_factors": ["string"]
}}
"""
