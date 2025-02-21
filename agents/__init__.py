import asyncio
from agents.data_aggregator import DataAggregator
from agents.trend_analyzer import TrendAnalyzer
from agents.risk_assessment import RiskAssessment
from agents.investment_recommendation import InvestmentRecommendation
from agents.news_sentiment import NewsSentiment
from agents.strategy_backtesting import StrategyBacktesting
from agents.alert_notification import AlertNotification

async def main():
    # Initialize agents
    data_aggregator = DataAggregator()
    trend_analyzer = TrendAnalyzer()
    risk_assessment = RiskAssessment()
    investment_recommendation = InvestmentRecommendation()
    news_sentiment = NewsSentiment()
    strategy_backtesting = StrategyBacktesting()
    alert_notification = AlertNotification()

    # Collect data
    market_data = await data_aggregator.collect_data()

    # Analyze trends and risks
    trends = await trend_analyzer.analyze(market_data)
    risks = await risk_assessment.evaluate(market_data)

    # Get news sentiment
    sentiment = await news_sentiment.analyze()

    # Generate investment recommendations
    recommendations = await investment_recommendation.recommend(market_data, trends, risks, sentiment)

    # Backtest strategies
    backtest_results = await strategy_backtesting.backtest(recommendations)

    # Send alerts
    await alert_notification.send_alert(recommendations, backtest_results)

    print("Crypto Investment Assistant process completed.")

if __name__ == "__main__":
    asyncio.run(main())