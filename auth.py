"""
Authentication module for user registration and login
"""
from werkzeug.security import generate_password_hash, check_password_hash
import re
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from backend.db import db
from backend.jwt_utils import JWTHandler

class AuthHandler:
    """Handle user authentication"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        return True, "Password is valid"
    
    @staticmethod
    def register_user(name, email, password):
        """Register a new user"""
        
        # Validate inputs
        if not name or len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if not AuthHandler.is_valid_email(email):
            return False, "Invalid email format"
        
        is_valid, msg = AuthHandler.is_valid_password(password)
        if not is_valid:
            return False, msg
        
        # Check if email already exists
        existing_user = db.execute_query(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )
        
        if existing_user:
            return False, "Email already registered"
        
        # Hash password and insert user
        password_hash = generate_password_hash(password)
        user_id = db.execute_insert(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, password_hash)
        )
        
        if user_id:
            return True, f"User registered successfully. User ID: {user_id}"
        else:
            return False, "Error registering user"
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return JWT token"""
        
        # Validate inputs
        if not AuthHandler.is_valid_email(email):
            return False, None, "Invalid email format"
        
        # Find user by email
        user = db.execute_query(
            "SELECT id, name, password_hash FROM users WHERE email = %s",
            (email,)
        )
        
        if not user:
            return False, None, "Invalid email or password"
        
        user = user[0]
        
        # Verify password
        if not check_password_hash(user['password_hash'], password):
            return False, None, "Invalid email or password"
        
        # Generate JWT token
        token = JWTHandler.generate_token(user['id'], email)
        
        if token:
            return True, token, f"Login successful. Welcome {user['name']}!"
        else:
            return False, None, "Error generating authentication token"
    
    @staticmethod
    def verify_user_token(token):
        """Verify JWT token and return user info"""
        payload = JWTHandler.verify_token(token)
        
        if not payload:
            return False, None
        
        user_id = payload.get('user_id')
        user = db.execute_query(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,)
        )
        
        if user:
            return True, user[0]
        else:
            return False, None
