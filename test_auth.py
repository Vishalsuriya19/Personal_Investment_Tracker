"""
Test suite for authentication
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(__file__).replace('/tests', ''))

from backend.auth import AuthHandler

class TestEmailValidation:
    """Test email validation"""
    
    def test_valid_email(self):
        """Test valid email"""
        assert AuthHandler.is_valid_email('test@example.com') == True
    
    def test_invalid_email_format(self):
        """Test invalid email format"""
        assert AuthHandler.is_valid_email('invalid-email') == False
        assert AuthHandler.is_valid_email('test@') == False
        assert AuthHandler.is_valid_email('@example.com') == False
    
    def test_valid_email_variations(self):
        """Test email format variations"""
        assert AuthHandler.is_valid_email('user.name@example.co.uk') == True
        assert AuthHandler.is_valid_email('user+tag@example.com') == True
        assert AuthHandler.is_valid_email('123@example.com') == True

class TestPasswordValidation:
    """Test password validation"""
    
    def test_strong_password(self):
        """Test strong password"""
        valid, msg = AuthHandler.is_valid_password('SecurePass123')
        assert valid == True
    
    def test_short_password(self):
        """Test short password"""
        valid, msg = AuthHandler.is_valid_password('Short1')
        assert valid == False
        assert 'at least 8 characters' in msg
    
    def test_no_uppercase(self):
        """Test password without uppercase"""
        valid, msg = AuthHandler.is_valid_password('securepass123')
        assert valid == False
        assert 'uppercase' in msg
    
    def test_no_digit(self):
        """Test password without digit"""
        valid, msg = AuthHandler.is_valid_password('SecurePass')
        assert valid == False
        assert 'digit' in msg

class TestJWTHandling:
    """Test JWT token handling"""
    
    def test_token_generation(self):
        """Test JWT token generation"""
        from backend.jwt_utils import JWTHandler
        
        token = JWTHandler.generate_token(1, 'test@example.com')
        assert token is not None
        assert isinstance(token, str)
    
    def test_token_verification(self):
        """Test JWT token verification"""
        from backend.jwt_utils import JWTHandler
        
        token = JWTHandler.generate_token(1, 'test@example.com')
        payload = JWTHandler.verify_token(token)
        
        assert payload is not None
        assert payload['user_id'] == 1
        assert payload['email'] == 'test@example.com'
    
    def test_invalid_token(self):
        """Test invalid token"""
        from backend.jwt_utils import JWTHandler
        
        payload = JWTHandler.verify_token('invalid.token.here')
        assert payload is None

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
