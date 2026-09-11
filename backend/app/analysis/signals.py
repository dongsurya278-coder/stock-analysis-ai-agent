"""Signal generation"""
from typing import Dict, Optional
from loguru import logger


class SignalGenerator:
    """Generates buy/sell signals"""
    
    @staticmethod
    def generate_signal(fundamental_score: float, technical_score: float, sentiment_score: float) -> Dict:
        """Generate composite signal from multiple factors"""
        try:
            # Weighted scoring
            weights = {"fundamental": 0.5, "technical": 0.3, "sentiment": 0.2}
            
            composite_score = (
                fundamental_score * weights["fundamental"] +
                technical_score * weights["technical"] +
                ((sentiment_score + 100) / 2) * weights["sentiment"]  # Normalize sentiment
            ) / 100
            
            # Determine signal
            if composite_score > 0.7:
                signal_strength = "strong_buy"
            elif composite_score > 0.6:
                signal_strength = "buy"
            elif composite_score > 0.4:
                signal_strength = "hold"
            elif composite_score > 0.3:
                signal_strength = "sell"
            else:
                signal_strength = "strong_sell"
            
            return {
                "signal_strength": signal_strength,
                "confidence_score": composite_score,
                "fundamental_score": fundamental_score,
                "technical_score": technical_score,
                "sentiment_score": sentiment_score
            }
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            raise
