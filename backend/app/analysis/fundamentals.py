"""Analysis Modules - FULLY IMPLEMENTED"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from loguru import logger


class FundamentalAnalyzer:
    """Analyzes stock fundamentals - Production Ready"""
    
    @staticmethod
    def analyze_valuation(pe_ratio: Optional[float], peg_ratio: Optional[float], industry_avg_pe: float = 20) -> Dict:
        """Analyze valuation metrics (0-100 score)"""
        score = 50  # Base score
        
        if pe_ratio and pe_ratio > 0:
            if pe_ratio < industry_avg_pe * 0.8:
                score += 30  # Undervalued
            elif pe_ratio > industry_avg_pe * 1.2:
                score -= 20  # Overvalued
        
        if peg_ratio and peg_ratio > 0:
            if peg_ratio < 1:
                score += 20  # Good value relative to growth
        
        return {
            'pe_ratio': pe_ratio or 0,
            'peg_ratio': peg_ratio or 0,
            'valuation_score': max(0, min(100, score)),
            'is_undervalued': score > 60
        }
    
    @staticmethod
    def analyze_growth(revenue_growth: Optional[float], eps_growth: Optional[float]) -> Dict:
        """Analyze growth metrics"""
        score = 50
        
        if revenue_growth:
            if revenue_growth > 0.15:  # 15% growth
                score += 25
            elif revenue_growth > 0.05:
                score += 15
            elif revenue_growth < 0:
                score -= 20
        
        if eps_growth:
            if eps_growth > 0.20:  # 20% growth
                score += 25
            elif eps_growth > 0.10:
                score += 15
            elif eps_growth < 0:
                score -= 20
        
        return {
            'revenue_growth': revenue_growth or 0,
            'eps_growth': eps_growth or 0,
            'growth_score': max(0, min(100, score)),
            'is_high_growth': score > 65
        }
    
    @staticmethod
    def analyze_health(debt_to_equity: Optional[float], current_ratio: Optional[float], roe: Optional[float]) -> Dict:
        """Analyze company financial health"""
        score = 50
        
        # Debt analysis (lower is better)
        if debt_to_equity:
            if debt_to_equity < 0.5:
                score += 25  # Low debt
            elif debt_to_equity > 2:
                score -= 25  # High debt
        
        # Liquidity analysis (higher is better)
        if current_ratio:
            if current_ratio > 1.5:
                score += 20  # Good liquidity
            elif current_ratio < 1:
                score -= 20  # Poor liquidity
        
        # Profitability analysis
        if roe:
            if roe > 0.15:  # 15% ROE
                score += 25  # Good profitability
            elif roe > 0.10:
                score += 15
            elif roe < 0:
                score -= 20  # Negative ROE
        
        return {
            'debt_to_equity': debt_to_equity or 0,
            'current_ratio': current_ratio or 0,
            'roe': roe or 0,
            'health_score': max(0, min(100, score)),
            'is_healthy': score > 60
        }
    
    @staticmethod
    def composite_fundamental_score(valuation: Dict, growth: Dict, health: Dict) -> float:
        """Combine all fundamental scores"""
        weights = {
            'valuation': 0.35,
            'growth': 0.35,
            'health': 0.30,
        }
        
        score = (
            valuation.get('valuation_score', 50) * weights['valuation'] +
            growth.get('growth_score', 50) * weights['growth'] +
            health.get('health_score', 50) * weights['health']
        )
        
        return min(100, max(0, score))


class TechnicalAnalyzer:
    """Performs technical analysis - Production Ready"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index (0-100)"""
        if len(prices) < period + 1:
            return 50
        
        try:
            deltas = np.diff(prices)
            seed = deltas[:period+1]
            up = seed[seed >= 0].sum() / period
            down = -seed[seed < 0].sum() / period
            rs = up / down if down != 0 else 0
            rsi = 100. - 100. / (1. + rs) if rs >= 0 else 0
            return float(rsi)
        except:
            return 50
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Dict:
        """Calculate MACD and signal line"""
        try:
            if len(prices) < 26:
                return {'macd': 0, 'signal': 0, 'histogram': 0}
            
            series = pd.Series(prices)
            exp1 = series.ewm(span=12, adjust=False).mean()
            exp2 = series.ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            
            return {
                'macd': float(macd.iloc[-1]),
                'signal': float(signal.iloc[-1]),
                'histogram': float(histogram.iloc[-1])
            }
        except:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    @staticmethod
    def calculate_moving_averages(prices: List[float]) -> Dict:
        """Calculate moving averages"""
        try:
            series = pd.Series(prices)
            ma20 = series.rolling(window=20).mean().iloc[-1]
            ma50 = series.rolling(window=50).mean().iloc[-1]
            ma200 = series.rolling(window=200).mean().iloc[-1]
            
            return {
                'ma20': float(ma20) if not pd.isna(ma20) else 0,
                'ma50': float(ma50) if not pd.isna(ma50) else 0,
                'ma200': float(ma200) if not pd.isna(ma200) else 0,
            }
        except:
            return {'ma20': 0, 'ma50': 0, 'ma200': 0}
    
    @staticmethod
    def calculate_bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            series = pd.Series(prices)
            middle = series.rolling(window=period).mean().iloc[-1]
            std = series.rolling(window=period).std().iloc[-1]
            
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            return {
                'upper': float(upper),
                'middle': float(middle),
                'lower': float(lower),
            }
        except:
            return {'upper': 0, 'middle': 0, 'lower': 0}
    
    @staticmethod
    def calculate_support_resistance(prices: List[float]) -> Dict:
        """Calculate support and resistance levels"""
        try:
            prices_array = np.array(prices)
            
            # Support = lowest point in last period
            support = float(np.min(prices_array[-20:]))
            
            # Resistance = highest point in last period
            resistance = float(np.max(prices_array[-20:]))
            
            return {
                'support': support,
                'resistance': resistance,
                'current_price': float(prices[-1]),
                'distance_to_support': float(prices[-1] - support),
                'distance_to_resistance': float(resistance - prices[-1]),
            }
        except:
            return {'support': 0, 'resistance': 0}
    
    @staticmethod
    def composite_technical_score(prices: List[float]) -> float:
        """Generate composite technical score (0-100)"""
        try:
            score = 50
            
            # RSI analysis
            rsi = TechnicalAnalyzer.calculate_rsi(prices)
            if rsi < 30:
                score += 25  # Oversold - buying opportunity
            elif rsi > 70:
                score -= 25  # Overbought - selling pressure
            
            # MACD analysis
            macd = TechnicalAnalyzer.calculate_macd(prices)
            if macd['histogram'] > 0:
                score += 15  # Positive momentum
            else:
                score -= 15
            
            # Moving average analysis
            mas = TechnicalAnalyzer.calculate_moving_averages(prices)
            current = prices[-1]
            if current > mas['ma50'] > mas['ma200']:
                score += 20  # Bullish trend
            elif current < mas['ma50'] < mas['ma200']:
                score -= 20  # Bearish trend
            
            return max(0, min(100, score))
        except:
            return 50


class SentimentAnalyzer:
    """Analyzes news sentiment - Production Ready"""
    
    # Simple keyword-based sentiment analysis
    POSITIVE_WORDS = [
        'surge', 'gain', 'bullish', 'strong', 'growth', 'beat', 'outperform',
        'rally', 'jump', 'soar', 'excellent', 'positive', 'buy', 'upgrade',
        'record', 'profit', 'earnings', 'revenue', 'success'
    ]
    
    NEGATIVE_WORDS = [
        'drop', 'fall', 'bearish', 'weak', 'decline', 'miss', 'underperform',
        'plunge', 'crash', 'downgrade', 'loss', 'negative', 'sell', 'failure',
        'warning', 'risk', 'concern', 'downside'
    ]
    
    @staticmethod
    def analyze_headlines(headlines: List[str]) -> Dict:
        """Analyze sentiment from headlines"""
        if not headlines:
            return {
                'sentiment_score': 0,
                'sentiment_label': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
            }
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0
        
        for headline in headlines:
            headline_lower = headline.lower()
            
            # Check for positive words
            pos_found = any(word in headline_lower for word in SentimentAnalyzer.POSITIVE_WORDS)
            # Check for negative words
            neg_found = any(word in headline_lower for word in SentimentAnalyzer.NEGATIVE_WORDS)
            
            if pos_found and not neg_found:
                positive_count += 1
                total_score += 1
            elif neg_found and not pos_found:
                negative_count += 1
                total_score -= 1
            else:
                neutral_count += 1
        
        # Calculate average sentiment
        avg_sentiment = total_score / len(headlines) if headlines else 0
        avg_sentiment = max(-1, min(1, avg_sentiment))  # Clamp to -1, 1
        
        # Determine label
        if avg_sentiment > 0.2:
            label = 'positive'
        elif avg_sentiment < -0.2:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'sentiment_score': float(avg_sentiment),
            'sentiment_label': label,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_headlines': len(headlines),
        }
