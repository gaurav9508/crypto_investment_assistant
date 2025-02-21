from telegram import Bot
from typing import Dict, Any, List
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.helpers import format_telegram_message

class AlertNotification:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.bot_token)

    async def send_alert(
        self,
        recommendations: List[Dict[str, Any]],
        backtest_results: Dict[str, Any],
        market_news: str = ""
    ) -> None:
        """
        Send investment recommendations and backtest results via Telegram.
        """
        try:
            # Format the message
            message = format_telegram_message(recommendations)
            
            # Add backtest results
            message += "\n\n📊 Backtest Results:\n"
            message += f"Overall Performance: {backtest_results['overall_performance']:.2%}\n"
            message += f"Success Rate: {backtest_results['success_rate']:.2%}\n"
            
            # Add market news if available
            if market_news:
                message += f"\n📰 Market News:\n{market_news}\n"
            
            # Send the message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )

        except Exception as e:
            print(f"Error sending alert: {e}")
