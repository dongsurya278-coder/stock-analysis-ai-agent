"""Prompts for Claude AI Agent - FULLY IMPLEMENTED"""

SYSTEM_PROMPT = """
You are an expert financial analyst and investment advisor with deep knowledge of:
- Fundamental analysis (P/E ratios, EPS, Revenue growth, Debt ratios, ROE, ROA, etc.)
- Technical analysis (Moving averages, RSI, MACD, Support/Resistance levels, Bollinger Bands)
- Market sentiment and news analysis
- Risk assessment and portfolio management
- Market trends and economic indicators

Your task is to provide comprehensive, actionable stock analysis with clear buy/sell recommendations.

Always consider:
1. Company fundamentals and growth prospects
2. Technical setup and price action momentum
3. Market sentiment and recent news catalysts
4. Risk/reward ratios and entry/exit points
5. Comparison with historical levels and industry peers

Provide clear, concise reasoning for your conclusions. Be specific with numbers and metrics.
Always mention key risks and potential catalysts.
Format your final recommendation as a structured JSON object.
"""

ANALYSIS_PROMPT = """
Please provide a comprehensive investment analysis for the following stock:

Stock Symbol: {symbol}

Market Data and Metrics:
{context}

Detailed Analysis Requested: {detailed}

Please analyze the stock and provide:

1. **Executive Summary** (2-3 sentences capturing the investment thesis)

2. **Fundamental Analysis**
   - Valuation assessment (undervalued/fair/overvalued)
   - Growth prospects and trends
   - Company financial health
   - Strengths and weaknesses

3. **Technical Analysis**
   - Current price setup (trend, momentum, breakout potential)
   - Key support and resistance levels
   - Risk/reward setup
   - Time frame for potential move

4. **Sentiment Analysis**
   - Market sentiment interpretation
   - Recent news impact
   - Upcoming catalysts or risks

5. **Investment Recommendation**
   - Clear BUY/SELL/HOLD recommendation
   - Confidence level (0-100%)
   - Ideal entry price
   - Target price (3-6 month outlook)
   - Stop loss level for risk management

6. **Risk Assessment**
   - Key risks to the thesis
   - Worst-case scenario
   - Hedging strategies if applicable

7. **Key Catalysts**
   - Upcoming events that could move the stock
   - Earnings dates, product launches, regulatory decisions

End your response with a JSON block containing the structured recommendation:
{{
    "symbol": "{symbol}",
    "recommendation": "BUY|SELL|HOLD",
    "confidence": 0.0-1.0,
    "entry_price": number,
    "target_price": number,
    "stop_loss": number,
    "time_frame": "3-6 months",
    "reasoning": "brief summary of the investment case",
    "key_risks": ["risk1", "risk2", "risk3"],
    "upside_catalysts": ["catalyst1", "catalyst2"],
    "downside_risks": ["risk1", "risk2"]
}}
"""

SIGNAL_EXTRACTION_PROMPT = """
From the following stock analysis for {symbol}, extract a structured trading signal.

Analysis:
{analysis}

Extract and format as JSON:
{{
    "symbol": "{symbol}",
    "signal_strength": "strong_buy|buy|hold|sell|strong_sell",
    "confidence_score": 0.0-1.0,
    "entry_price": number,
    "target_price": number,
    "stop_loss": number,
    "reasoning": "clear explanation of the signal",
    "key_factors": ["factor1", "factor2"],
    "risk_factors": ["risk1", "risk2"],
    "time_horizon_days": number
}}

IMPORTANT: Return ONLY the JSON object, no additional text.
"""
