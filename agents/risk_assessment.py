import pandas as pd
import numpy as np
from typing import Dict
from utils.helpers import calculate_risk_metrics

class RiskAssessment:
    def __init__(self):
        self.risk_weights = {
            'volatility': 0.4,
            'market_cap': 0.3,
            'volume': 0.3
        }

    async def evaluate(self, market_data: pd.DataFrame) -> Dict[str, float]:
        """
        Evaluate risk scores for cryptocurrencies.
        """
        risk_scores = {}
        
        for _, row in market_data.iterrows():
            symbol = row['symbol'].upper()
            
            # Calculate risk metrics
            volatility = row['price_change_percentage_24h'] / 100 if 'price_change_percentage_24h' in row else 0
            market_cap_rank = row['market_cap_rank'] if 'market_cap_rank' in row else 100
            volume = row['total_volume'] if 'total_volume' in row else 0
            
            # Normalize metrics
            normalized_volatility = abs(volatility)
            normalized_market_cap = market_cap_rank / 100
            normalized_volume = 1 - (volume / market_data['total_volume'].max())
            
            # Calculate weighted risk score
            risk_score = (
                self.risk_weights['volatility'] * normalized_volatility +
                self.risk_weights['market_cap'] * normalized_market_cap +
                self.risk_weights['volume'] * normalized_volume
            )
            
            risk_scores[symbol] = min(max(risk_score, 0), 1)  # Ensure score is between 0 and 1
        
        return risk_scores
