import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
COINBASE_API_SECRET = os.getenv('COINBASE_API_SECRET')
COINBASE_API_PASSPHRASE = os.getenv('COINBASE_API_PASSPHRASE')

# API URLs
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
COINBASE_API_URL = "https://api.pro.coinbase.com"

# Add any other global settings here

