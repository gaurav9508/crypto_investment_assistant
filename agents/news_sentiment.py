import requests
import nltk
import hmac
import hashlib
import time
import base64
from typing import Dict
from nltk.sentiment import SentimentIntensityAnalyzer
from config.settings import (
    COINBASE_API_URL, 
    COINBASE_API_KEY, 
    COINBASE_API_SECRET, 
    COINBASE_API_PASSPHRASE
)

class NewsSentiment:
    def __init__(self):
        nltk.download('vader_lexicon', quiet=True)
        self.sia = SentimentIntensityAnalyzer()
        self.coinbase_api_url = COINBASE_API_URL

    def get_coinbase_auth_headers(self, method: str, endpoint: str, body: str = '') -> Dict[str, str]:
        """
        Generate authentication headers for Coinbase API.
        """
        timestamp = str(int(time.time()))
        message = timestamp + method + endpoint + body
        signature = hmac.new(
            COINBASE_API_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

        return {
            'CB-ACCESS-KEY': COINBASE_API_KEY,
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': COINBASE_API_PASSPHRASE,
        }

    async def analyze(self) -> Dict[str, float]:
        """
        Analyze market sentiment using Coinbase trade data.
        """
        try:
            endpoint = '/products/BTC-USD/trades'
            headers = self.get_coinbase_auth_headers('GET', endpoint)
            response = requests.get(f"{self.coinbase_api_url}{endpoint}", headers=headers)
            response.raise_for_status()
            trades_data = response.json()

            # Analyze sentiment based on price movements
            sentiments = []
            for trade in trades_data[:100]:  # Analyze last 100 trades
                price_change = float(trade['price']) - float(trades_data[0]['price'])
                if price_change > 0:
                    sentiments.append(1)  # Positive sentiment
                elif price_change < 0:
                    sentiments.append(-1)  # Negative sentiment
                else:
                    sentiments.append(0)  # Neutral sentiment

            # Calculate average sentiment
            avg_sentiment = sum(sentiments) / len(sentiments)
            normalized_sentiment = avg_sentiment / max(abs(min(sentiments)), abs(max(sentiments)))

            return {"BTC": normalized_sentiment}

        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {"BTC": 0.0}  # Neutral sentiment as fallback

    async def get_market_news(self) -> str:
        """
        Get latest market news (placeholder function).
        """
        return "Check https://www.coinbase.com/news for the latest crypto market news."
