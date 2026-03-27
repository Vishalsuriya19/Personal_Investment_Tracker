"""
NLP Report Generation Module
Generates AI-based portfolio analysis reports
"""
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from ml_models.predict import InvestmentPredictor
from datetime import datetime

class ReportGenerator:
    """Generate AI-based portfolio analysis reports"""
    
    @staticmethod
    def generate_insights(risk_analysis, predictions):
        """Generate investment insights"""
        
        insights = []
        risk_level = risk_analysis.get('risk_level', 'Medium')
        total_amount = risk_analysis.get('total_amount', 0)
        num_investments = risk_analysis.get('num_investments', 0)
        
        # Risk-based insights
        if risk_level == 'High':
            insights.append(
                "⚠️ Your portfolio has HIGH risk due to concentration. "
                "Consider diversifying to reduce exposure."
            )
        elif risk_level == 'Medium':
            insights.append(
                "💡 Your portfolio has MODERATE risk. Balance is reasonable. "
                "Monitor for market changes."
            )
        else:
            insights.append(
                "✓ Your portfolio has LOW risk. Good diversification. "
                "Consider strategic additions."
            )
        
        # Investment count
        if num_investments < 3:
            insights.append(
                "📊 You have limited diversification. "
                "Consider adding 2-3 more investments for better spread."
            )
        elif num_investments > 10:
            insights.append(
                "📈 You have good diversification across multiple investments."
            )
        
        # Prediction-based insights
        positive_predictions = sum(1 for p in predictions if p['price_growth_percent'] > 0)
        negative_predictions = len(predictions) - positive_predictions
        
        if positive_predictions > negative_predictions:
            insights.append(
                f"📈 {positive_predictions} of your investments show positive growth potential."
            )
        elif negative_predictions > positive_predictions:
            insights.append(
                f"📉 {negative_predictions} investments may see price decline. "
                f"Review your holdings."
            )
        
        # High-risk stocks
        high_risk_stocks = [p['stock_name'] for p in predictions if p['risk_level'] == 'High']
        if high_risk_stocks:
            insights.append(
                f"⚠️ High-risk holdings detected: {', '.join(high_risk_stocks)}. "
                f"Consider reducing exposure."
            )
        
        return insights
    
    @staticmethod
    def generate_recommendations(predictions, risk_analysis):
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Sort predictions by risk
        high_risk = [p for p in predictions if p['risk_level'] == 'High']
        low_risk = [p for p in predictions if p['risk_level'] == 'Low']
        
        if high_risk:
            stocks = ', '.join([p['stock_name'] for p in high_risk[:3]])
            recommendations.append(
                f"REDUCE: Consider decreasing exposure to {stocks}"
            )
        
        if low_risk and len(low_risk) > 0:
            stocks = ', '.join([p['stock_name'] for p in low_risk[:3]])
            recommendations.append(
                f"INCREASE: These have lower risk profile: {stocks}"
            )
        
        # Rebalancing recommendation
        total_amount = risk_analysis.get('total_amount', 0)
        num_investments = risk_analysis.get('num_investments', 0)
        
        if num_investments > 0:
            avg_per_investment = total_amount / num_investments
            recommendations.append(
                f"REBALANCE: Target allocation ~₹{avg_per_investment:,.0f} per investment"
            )
        
        # Growth strategy
        positive_preds = sum(1 for p in predictions if p['price_growth_percent'] > 10)
        if positive_preds > 0:
            recommendations.append(
                "GROWTH: Focus on investments with >10% growth potential"
            )
        
        return recommendations
    
    @staticmethod
    def generate_report(user_data, predictions, risk_analysis):
        """
        Generate complete portfolio report
        
        Args:
            user_data: User information
            predictions: List of predictions
            risk_analysis: Risk analysis results
        
        Returns:
            Report dictionary
        """
        
        # Generate insights and recommendations
        insights = ReportGenerator.generate_insights(risk_analysis, predictions)
        recommendations = ReportGenerator.generate_recommendations(
            predictions, risk_analysis
        )
        
        # Build report text
        report_text = ReportGenerator._build_report_text(
            user_data, insights, recommendations, risk_analysis, predictions
        )
        
        # Determine overall risk assessment
        risk_level = risk_analysis.get('risk_level', 'Medium')
        risk_score = risk_analysis.get('risk_score', 50)
        
        report = {
            'report_text': report_text,
            'risk_assessment': risk_level,
            'risk_score': risk_score,
            'insights': insights,
            'recommendations': recommendations,
            'predictions': predictions,
            'portfolio_value': risk_analysis.get('total_amount', 0),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return report
    
    @staticmethod
    def _build_report_text(user_data, insights, recommendations, risk_analysis, predictions):
        """Build formatted report text"""
        
        date = datetime.now().strftime('%B %d, %Y')
        name = user_data.get('name', 'Valued Investor')
        total_amount = risk_analysis.get('total_amount', 0)
        num_investments = risk_analysis.get('num_investments', 0)
        risk_level = risk_analysis.get('risk_level', 'Medium')
        
        report_lines = [
            f"📋 INVESTMENT PORTFOLIO ANALYSIS REPORT",
            f"{'='*50}",
            f"Date: {date}",
            f"Investor: {name}",
            f"",
            f"PORTFOLIO SUMMARY",
            f"{'-'*50}",
            f"Total Portfolio Value: ₹{total_amount:,.2f}",
            f"Number of Investments: {num_investments}",
            f"Overall Risk Level: {risk_level}",
            f"",
            f"KEY INSIGHTS",
            f"{'-'*50}",
        ]
        
        for i, insight in enumerate(insights, 1):
            report_lines.append(f"{i}. {insight}")
        
        report_lines.extend([
            f"",
            f"RECOMMENDATIONS",
            f"{'-'*50}",
        ])
        
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.extend([
            f"",
            f"PREDICTIONS (30-DAY OUTLOOK)",
            f"{'-'*50}",
        ])
        
        for pred in predictions[:5]:  # Show top 5
            growth = pred.get('price_growth_percent', 0)
            stock = pred.get('stock_name', 'N/A')
            report_lines.append(
                f"{stock}: {growth:+.2f}% growth | Risk: {pred.get('risk_level', 'N/A')}"
            )
        
        report_lines.extend([
            f"",
            f"DISCLAIMER",
            f"{'-'*50}",
            f"This is an AI-generated analysis based on historical data and patterns.",
            f"Actual market conditions may vary. Always consult with a financial advisor.",
            f"Past performance does not guarantee future results.",
        ])
        
        return '\n'.join(report_lines)

if __name__ == '__main__':
    # Example usage
    sample_user = {'name': 'John Investor'}
    sample_predictions = [
        {
            'stock_name': 'AAPL',
            'current_price': 150,
            'predicted_price': 165,
            'price_growth_percent': 10,
            'risk_level': 'Low',
            'profit_probability': 75
        },
        {
            'stock_name': 'GOOGL',
            'current_price': 100,
            'predicted_price': 95,
            'price_growth_percent': -5,
            'risk_level': 'Medium',
            'profit_probability': 45
        }
    ]
    sample_risk = {
        'risk_level': 'Medium',
        'risk_score': 55,
        'total_amount': 25000,
        'num_investments': 2
    }
    
    report = ReportGenerator.generate_report(
        sample_user, sample_predictions, sample_risk
    )
    print(report['report_text'])
