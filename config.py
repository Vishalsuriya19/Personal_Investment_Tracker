"""
Configuration file for Investment Tracker Application
"""
import os
from datetime import timedelta

# Database Configuration
DATABASE_HOST = os.getenv('DB_HOST', 'localhost')
DATABASE_USER = os.getenv('DB_USER', 'root')
DATABASE_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DATABASE_NAME = os.getenv('DB_NAME', 'investment_tracker')
DATABASE_PORT = int(os.getenv('DB_PORT', 3306))

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-in-production')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

# Streamlit Configuration
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')

# ML Model Configuration
MODEL_UPDATE_INTERVAL_DAYS = 7  # Retrain model every 7 days
PREDICTION_HORIZON_DAYS = 30  # Predict for 30 days ahead

# Application Settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
TESTING = os.getenv('TESTING', 'False') == 'True'
