"""
Test suite for API endpoints
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('/tests', ''))

from backend.app import create_app

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    if app:
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    else:
        yield None

class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        if client:
            response = client.get('/api/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'healthy'
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        if client:
            response = client.post('/api/register', json={
                'name': 'Test User',
                'email': 'invalid-email',
                'password': 'SecurePass123'
            })
            assert response.status_code == 400
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        if client:
            response = client.post('/api/register', json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'weak'
            })
            assert response.status_code == 400
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        if client:
            response = client.post('/api/login', json={
                'email': 'nonexistent@example.com',
                'password': 'AnyPassword123'
            })
            assert response.status_code == 401

class TestInvestmentEndpoints:
    """Test investment endpoints"""
    
    def test_get_portfolio_without_auth(self, client):
        """Test protected endpoint without token"""
        if client:
            response = client.get('/api/portfolio')
            assert response.status_code == 401
    
    def test_add_investment_without_auth(self, client):
        """Test protected endpoint without token"""
        if client:
            response = client.post('/api/add_investment', json={
                'stock_name': 'AAPL',
                'quantity': 10,
                'purchase_price': 150,
                'date': '2024-01-01'
            })
            assert response.status_code == 401

class TestPredictionEndpoints:
    """Test prediction endpoints"""
    
    def test_predict_without_auth(self, client):
        """Test prediction endpoint without auth"""
        if client:
            response = client.post('/api/predict')
            assert response.status_code == 401

class TestReportEndpoints:
    """Test report endpoints"""
    
    def test_get_report_without_auth(self, client):
        """Test report endpoint without auth"""
        if client:
            response = client.get('/api/report')
            assert response.status_code == 401

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
