"""Technical analysis"""
import pandas as pd
import numpy as np
from typing import Dict, Optional
from loguru import logger


class TechnicalAnalyzer:
    """Performs technical analysis"""
    
    @staticmethod
    def calculate_rsi(prices: list, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        try:
            deltas = np.diff(prices)
            seed = deltas[:period+1]
            up = seed[seed >= 0].sum() / period
            down = -seed[seed < 0].sum() / period
            rs = up / down if down != 0 else 0
            rsi = 100. - 100. / (1. + rs)
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return None
    
    @staticmethod
    def calculate_macd(prices: list, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD"""
        try:
            exp1 = pd.Series(prices).ewm(span=fast).mean()
            exp2 = pd.Series(prices).ewm(span=slow).mean()
            macd = exp1 - exp2
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            
            return {
                "macd": macd.iloc[-1],
                "signal": signal_line.iloc[-1],
                "histogram": histogram.iloc[-1]
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return None
    
    @staticmethod
    def calculate_moving_averages(prices: list) -> Dict:
        """Calculate moving averages"""
        try:
            ma50 = pd.Series(prices).rolling(window=50).mean().iloc[-1]
            ma200 = pd.Series(prices).rolling(window=200).mean().iloc[-1]
            return {
                "ma50": ma50,
                "ma200": ma200
            }
        except Exception as e:
            logger.error(f"Error calculating MAs: {e}")
            return None
