"""
ML Model Training Module
Trains regression model for price prediction and risk scoring model
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))

class PricePredictor:
    """Train and predict stock prices using regression models"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_path = os.path.join(
            os.path.dirname(__file__), 'regression.pkl'
        )
        self.scaler_path = os.path.join(
            os.path.dirname(__file__), 'scaler.pkl'
        )
    
    @staticmethod
    def generate_synthetic_data(n_samples=500):
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
        
        data = {
            'days_held': np.random.randint(1, 365, n_samples),
            'market_sentiment': np.random.uniform(-1, 1, n_samples),
            'volatility': np.random.uniform(0, 0.3, n_samples),
            'volume': np.random.randint(1000, 1000000, n_samples),
            'rsi': np.random.uniform(20, 80, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Create synthetic target (price growth percentage)
        df['price_growth'] = (
            0.02 * df['days_held'] +
            5 * df['market_sentiment'] +
            -10 * df['volatility'] +
            0.00001 * df['volume'] +
            0.1 * df['rsi'] +
            np.random.normal(0, 5, n_samples)
        )
        
        return df
    
    def train(self):
        """Train the regression model"""
        print("📊 Training Price Prediction Model...")
        
        # Generate synthetic data
        df = self.generate_synthetic_data()
        
        X = df[['days_held', 'market_sentiment', 'volatility', 'volume', 'rsi']]
        y = df['price_growth']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train multiple models and choose the best
        models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        best_score = -float('inf')
        best_model_name = None
        
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            score = model.score(X_test_scaled, y_test)
            print(f"  {name} R² Score: {score:.4f}")
            
            if score > best_score:
                best_score = score
                best_model_name = name
                self.model = model
        
        print(f"✓ Best model: {best_model_name} (R² = {best_score:.4f})")
        
        # Save models
        self.save()
        
        return True
    
    def predict(self, features_dict):
        """
        Predict stock price growth
        features_dict: dict with keys - days_held, market_sentiment, volatility, volume, rsi
        """
        if not self.model:
            self.load()
        
        if not self.model:
            print("✗ Model not loaded")
            return None
        
        features = np.array([[
            features_dict.get('days_held', 0),
            features_dict.get('market_sentiment', 0),
            features_dict.get('volatility', 0.1),
            features_dict.get('volume', 100000),
            features_dict.get('rsi', 50)
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return float(prediction)
    
    def save(self):
        """Save model and scaler to disk"""
        if self.model and self.scaler:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"✓ Model saved to {self.model_path}")
    
    def load(self):
        """Load model and scaler from disk"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("✓ Model loaded successfully")
            return True
        return False

class RiskScorer:
    """Calculate investment risk score"""
    
    @staticmethod
    def calculate_risk(portfolio_data):
        """
        Calculate risk level based on portfolio composition
        portfolio_data: dict with investment information
        """
        
        # Simple risk calculation
        total_amount = portfolio_data.get('total_amount', 0)
        
        if total_amount == 0:
            return 'Low', 20
        
        # Calculate concentration risk
        investments = portfolio_data.get('investments', [])
        if investments:
            largest_investment = max([inv.get('amount', 0) for inv in investments])
            concentration = (largest_investment / total_amount) * 100
        else:
            concentration = 0
        
        # Risk scoring logic
        risk_score = concentration * 0.4 + np.random.uniform(0, 30)
        
        if risk_score < 30:
            risk_level = 'Low'
        elif risk_score < 60:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        return risk_level, min(100, risk_score)

if __name__ == '__main__':
    # Train model
    predictor = PricePredictor()
    predictor.train()
    
    # Test prediction
    test_features = {
        'days_held': 30,
        'market_sentiment': 0.5,
        'volatility': 0.15,
        'volume': 500000,
        'rsi': 55
    }
    
    prediction = predictor.predict(test_features)
    print(f"Predicted price growth: {prediction:.2f}%")
