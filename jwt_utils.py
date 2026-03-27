"""
JWT (JSON Web Token) utilities for authentication
"""
import jwt
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

class JWTHandler:
    """Handle JWT token generation and validation"""
    
    @staticmethod
    def generate_token(user_id, email):
        """Generate a JWT token for a user"""
        try:
            payload = {
                'user_id': user_id,
                'email': email,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            return token
        except Exception as e:
            print(f"✗ Error generating token: {e}")
            return None
    
    @staticmethod
    def verify_token(token):
        """Verify a JWT token and return the payload"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            print("✗ Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"✗ Invalid token: {e}")
            return None
    
    @staticmethod
    def get_user_id_from_token(token):
        """Extract user_id from token"""
        payload = JWTHandler.verify_token(token)
        if payload:
            return payload.get('user_id')
        return None
