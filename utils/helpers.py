import pandas as pd
import numpy as np
from typing import Dict, List

def preprocess_market_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the market data for analysis.
    """
    # Add normalized columns
    if 'market_cap' in data.columns:
        data['market_cap_normalized'] = (data['market_cap'] - data['market_cap'].min()) / \
                                      (data['market_cap'].max() - data['market_cap'].min())
    
    # Handle missing values
    data = data.fillna(method='ffill')
    
    return data

def calculate_risk_metrics(price_data: pd.Series) -> Dict[str, float]:
    """
    Calculate various risk metrics for a given price series.
    """
    returns = price_data.pct_change().dropna()
    
    risk_metrics = {
        'volatility': returns.std(),
        'var_95': np.percentile(returns, 5),
        'max_drawdown': (price_data / price_data.expanding(min_periods=1).max()).min() - 1
    }
    
    return risk_metrics

def format_telegram_message(recommendations: List[dict]) -> str:
    """
    Format recommendations for Telegram message.
    """
    message = "🚀 Crypto Investment Recommendations:\n\n"
    
    for rec in recommendations:
        message += f"💎 {rec['symbol']}: {rec['recommendation']}\n"
        message += f"Risk Score: {rec['risk_score']:.2f}\n"
        message += f"Confidence: {rec['confidence']:.2%}\n\n"
    
    message += "\n⚠️ This is not financial advice. Always DYOR (Do Your Own Research)."
    
    return message
