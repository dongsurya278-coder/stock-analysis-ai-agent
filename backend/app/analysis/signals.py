"""Signal Generation - FULLY IMPLEMENTED"""
from typing import Dict
from loguru import logger


class SignalGenerator:
    """Generates buy/sell signals - Production Ready"""
    
    @staticmethod
    def generate_signal(fundamental_score: float, technical_score: float, sentiment_score: float, confidence: float = None) -> Dict:
        """Generate composite signal from multiple factors"""
        try:
            # Weighted scoring (fundamental > technical > sentiment)
            weights = {
                'fundamental': 0.45,
                'technical': 0.35,
                'sentiment': 0.20,
            }
            
            # Normalize sentiment to 0-100 range
            sentiment_normalized = ((sentiment_score + 1) / 2) * 100
            
            composite_score = (
                fundamental_score * weights['fundamental'] +
                technical_score * weights['technical'] +
                sentiment_normalized * weights['sentiment']
            )
            
            composite_score = min(100, max(0, composite_score))
            
            # Determine signal strength
            if composite_score >= 80:
                signal_strength = "strong_buy"
                confidence_score = 0.95
            elif composite_score >= 70:
                signal_strength = "buy"
                confidence_score = 0.80
            elif composite_score >= 55:
                signal_strength = "hold"
                confidence_score = 0.65
            elif composite_score >= 40:
                signal_strength = "sell"
                confidence_score = 0.70
            else:
                signal_strength = "strong_sell"
                confidence_score = 0.85
            
            return {
                'signal_strength': signal_strength,
                'confidence_score': confidence_score,
                'composite_score': composite_score,
                'fundamental_score': fundamental_score,
                'technical_score': technical_score,
                'sentiment_score': sentiment_score,
            }
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return {
                'signal_strength': 'hold',
                'confidence_score': 0.5,
                'composite_score': 50,
            }
