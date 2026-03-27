"""
Prediction module for making investment predictions
"""
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from ml_models.train_model import PricePredictor, RiskScorer
from backend.db import db
from datetime import datetime, timedelta
import random

class InvestmentPredictor:
    """Main predictor class for generating investment predictions"""
    
    def __init__(self):
        self.price_predictor = PricePredictor()
        self.price_predictor.load()
    
    def predict_for_portfolio(self, user_id, investment_data):
        """
        Generate predictions for all investments in portfolio
        
        Args:
            user_id: User ID
            investment_data: List of investment dictionaries
        
        Returns:
            List of predictions
        """
        predictions = []
        
        for investment in investment_data:
            stock_name = investment.get('stock_name')
            current_price = investment.get('purchase_price', 100)
            amount = investment.get('amount', 0)
            purchase_date = investment.get('date')
            
            # Calculate days held
            if purchase_date:
                purchase_dt = datetime.strptime(str(purchase_date), '%Y-%m-%d')
                days_held = (datetime.now() - purchase_dt).days
            else:
                days_held = 0
            
            # Predict price growth
            features = {
                'days_held': min(days_held, 365),
                'market_sentiment': random.uniform(-0.5, 0.5),
                'volatility': random.uniform(0.05, 0.25),
                'volume': random.randint(100000, 1000000),
                'rsi': random.uniform(30, 70)
            }
            
            price_growth = self.price_predictor.predict(features)
            predicted_price = current_price * (1 + price_growth / 100)
            
            # Calculate profit probability
            profit_prob = min(100, max(0, 50 + (price_growth / 2)))
            
            # Determine risk level
            if price_growth > 10:
                risk_level = 'Low'
            elif price_growth > 0:
                risk_level = 'Medium'
            else:
                risk_level = 'High'
            
            predictions.append({
                'user_id': user_id,
                'stock_name': stock_name,
                'current_price': float(current_price),
                'predicted_price': float(predicted_price),
                'price_growth_percent': float(price_growth),
                'risk_level': risk_level,
                'profit_probability': float(profit_prob),
                'date': datetime.now().strftime('%Y-%m-%d')
            })
        
        return predictions
    
    def save_predictions(self, predictions):
        """Save predictions to database"""
        for pred in predictions:
            db.execute_insert(
                """INSERT INTO predictions 
                   (user_id, stock_name, current_price, predicted_price, 
                    risk_level, profit_probability, date) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    pred['user_id'],
                    pred['stock_name'],
                    pred['current_price'],
                    pred['predicted_price'],
                    pred['risk_level'],
                    pred['profit_probability'],
                    pred['date']
                )
            )
    
    @staticmethod
    def portfolio_risk_analysis(user_id, investment_data):
        """Analyze overall portfolio risk"""
        
        total_amount = sum([inv.get('amount', 0) for inv in investment_data])
        
        portfolio_data = {
            'total_amount': total_amount,
            'investments': investment_data
        }
        
        risk_level, risk_score = RiskScorer.calculate_risk(portfolio_data)
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'total_amount': total_amount,
            'num_investments': len(investment_data)
        }

if __name__ == '__main__':
    # Example usage
    predictor = InvestmentPredictor()
    
    sample_investments = [
        {
            'stock_name': 'AAPL',
            'purchase_price': 150,
            'amount': 15000,
            'date': '2024-01-01'
        },
        {
            'stock_name': 'GOOGL',
            'purchase_price': 100,
            'amount': 10000,
            'date': '2024-02-15'
        }
    ]
    
    predictions = predictor.predict_for_portfolio(1, sample_investments)
    for pred in predictions:
        print(f"{pred['stock_name']}: ${pred['current_price']:.2f} → ${pred['predicted_price']:.2f}")
