"""
Test suite for ML models
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('/tests', ''))

from ml_models.train_model import PricePredictor, RiskScorer
from ml_models.nlp_report import ReportGenerator

class TestPricePredictor:
    """Test price prediction model"""
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        df = PricePredictor.generate_synthetic_data(100)
        
        assert len(df) == 100
        assert 'price_growth' in df.columns
        assert 'days_held' in df.columns
        assert 'market_sentiment' in df.columns
    
    def test_model_prediction(self):
        """Test model can make predictions"""
        predictor = PricePredictor()
        predictor.train()
        
        features = {
            'days_held': 30,
            'market_sentiment': 0.5,
            'volatility': 0.15,
            'volume': 500000,
            'rsi': 55
        }
        
        prediction = predictor.predict(features)
        assert prediction is not None
        assert isinstance(prediction, (int, float))

class TestRiskScorer:
    """Test risk scoring"""
    
    def test_low_risk_calculation(self):
        """Test low risk scenario"""
        portfolio = {
            'total_amount': 100000,
            'investments': [
                {'amount': 25000},
                {'amount': 25000},
                {'amount': 25000},
                {'amount': 25000}
            ]
        }
        
        risk_level, score = RiskScorer.calculate_risk(portfolio)
        assert risk_level in ['Low', 'Medium', 'High']
        assert 0 <= score <= 100
    
    def test_high_risk_concentration(self):
        """Test high risk concentration"""
        portfolio = {
            'total_amount': 100000,
            'investments': [
                {'amount': 90000},
                {'amount': 10000}
            ]
        }
        
        risk_level, score = RiskScorer.calculate_risk(portfolio)
        assert risk_level == 'High'
        assert score > 60

class TestReportGenerator:
    """Test report generation"""
    
    def test_insights_generation(self):
        """Test insight generation"""
        risk_analysis = {
            'risk_level': 'Medium',
            'total_amount': 50000,
            'num_investments': 3
        }
        
        predictions = [
            {
                'stock_name': 'AAPL',
                'price_growth_percent': 10,
                'risk_level': 'Low',
                'profit_probability': 75
            },
            {
                'stock_name': 'GOOGL',
                'price_growth_percent': -5,
                'risk_level': 'Medium',
                'profit_probability': 45
            }
        ]
        
        insights = ReportGenerator.generate_insights(risk_analysis, predictions)
        assert len(insights) > 0
        assert all(isinstance(i, str) for i in insights)
    
    def test_recommendations_generation(self):
        """Test recommendation generation"""
        predictions = [
            {
                'stock_name': 'AAPL',
                'price_growth_percent': 10,
                'risk_level': 'Low'
            },
            {
                'stock_name': 'GOOGL',
                'price_growth_percent': -5,
                'risk_level': 'High'
            }
        ]
        
        risk_analysis = {
            'risk_level': 'High',
            'total_amount': 50000,
            'num_investments': 2
        }
        
        recs = ReportGenerator.generate_recommendations(predictions, risk_analysis)
        assert len(recs) > 0
        assert all(isinstance(r, str) for r in recs)
    
    def test_report_generation(self):
        """Test complete report generation"""
        user_data = {'name': 'Test User'}
        
        predictions = [
            {
                'stock_name': 'AAPL',
                'current_price': 150,
                'predicted_price': 165,
                'price_growth_percent': 10,
                'risk_level': 'Low',
                'profit_probability': 75
            }
        ]
        
        risk_analysis = {
            'risk_level': 'Low',
            'risk_score': 30,
            'total_amount': 50000,
            'num_investments': 1
        }
        
        report = ReportGenerator.generate_report(user_data, predictions, risk_analysis)
        
        assert report['risk_assessment'] == 'Low'
        assert 'AAPL' in report['report_text']
        assert len(report['insights']) > 0
        assert len(report['recommendations']) > 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
