import google.generativeai as genai
from typing import Dict, Any, List
from config.settings import GEMINI_API_KEY

class InvestmentRecommendation:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def recommend(
        self,
        market_data: Dict[str, Any],
        trends: Dict[str, Dict[str, Any]],
        risks: Dict[str, float],
        sentiment: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Generate investment recommendations using Gemini model.
        """
        try:
            # Prepare input for Gemini model
            prompt = self._prepare_prompt(market_data, trends, risks, sentiment)
            
            # Generate recommendations
            response = self.model.generate_content(prompt)
            recommendations = self._parse_recommendations(response.text)
            
            return recommendations

        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []

    def _prepare_prompt(
        self,
        market_data: Dict[str, Any],
        trends: Dict[str, Dict[str, Any]],
        risks: Dict[str, float],
        sentiment: Dict[str, float]
    ) -> str:
        """
        Prepare the prompt for the Gemini model.
        """
        return f"""
        Based on the following market data and analysis, recommend the top cryptocurrencies to invest in:

        Market Data:
        {market_data}

        Technical Trends:
        {trends}

        Risk Assessment:
        {risks}

        Market Sentiment:
        {sentiment}

        Please provide recommendations in the following format:
        1. [Symbol]: [Reason] | Risk: [Score] | Confidence: [Level]
        2. [Symbol]: [Reason] | Risk: [Score] | Confidence: [Level]
        ...
        """

    def _parse_recommendations(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse the model's response into structured recommendations.
        """
        recommendations = []
        lines = response_text.strip().split('\n')
        
        for line in lines:
            if not line.strip() or not line[0].isdigit():
                continue
                
            try:
                parts = line.split('|')
                if len(parts) >= 3:
                    symbol_reason = parts[0].split(':')
                    risk = parts[1].split(':')[1].strip()
                    confidence = parts[2].split(':')[1].strip()
                    
                    recommendations.append({
                        'symbol': symbol_reason[0].split('.')[1].strip(),
                        'recommendation': symbol_reason[1].strip(),
                        'risk_score': float(risk.replace('%', '')) / 100,
                        'confidence': float(confidence.replace('%', '')) / 100
                    })
            except Exception as e:
                print(f"Error parsing recommendation line: {e}")
                continue
        
        return recommendations
