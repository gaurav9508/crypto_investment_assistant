import pandas as pd
import ta
from typing import Dict, Any

class TrendAnalyzer:
    def __init__(self):
        self.indicators = {
            'sma': 20,
            'rsi': 14,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9
        }

    async def analyze(self, market_data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Analyze market trends using technical indicators.
        """
        trends = {}
        
        for _, row in market_data.iterrows():
            symbol = row['symbol'].upper()
            price = row['current_price']
            
            # Calculate technical indicators
            sma = ta.trend.sma_indicator(pd.Series(price), window=self.indicators['sma'])
            rsi = ta.momentum.rsi(pd.Series(price), window=self.indicators['rsi'])
            macd = ta.trend.macd_diff(pd.Series(price), 
                                    window_fast=self.indicators['macd_fast'],
                                    window_slow=self.indicators['macd_slow'],
                                    window_sign=self.indicators['macd_signal'])
            
            # Determine trend signals
            trends[symbol] = {
                'price': price,
                'trend': 'bullish' if price > sma.iloc[-1] else 'bearish',
                'strength': 'strong' if abs(rsi.iloc[-1] - 50) > 20 else 'weak',
                'momentum': 'positive' if macd.iloc[-1] > 0 else 'negative',
                'overbought': rsi.iloc[-1] > 70,
                'oversold': rsi.iloc[-1] < 30
            }
        
        return trends
