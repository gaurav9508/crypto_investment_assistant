import requests
import pandas as pd

class DataAggregator:
    def __init__(self):
        self.coingecko_api = "https://api.coingecko.com/api/v3"

    async def collect_data(self):
        # Collect data from CoinGecko API (free tier)
        url = f"{self.coingecko_api}/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": False
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
