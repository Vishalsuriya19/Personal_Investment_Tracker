"""
Flask backend application for Investment Tracker
"""
from flask import Flask, jsonify
from flask_cors import CORS
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from config import FLASK_SECRET_KEY, FLASK_ENV, DEBUG
from backend.db import db
from backend.routes import api_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['ENV'] = FLASK_ENV
    app.config['DEBUG'] = DEBUG
    
    # Enable CORS for Streamlit frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Database connection
    if not db.connect():
        print("Failed to connect to database")
        return None
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
    
    @app.teardown_appcontext
    def close_connection(exception):
        """Close database connection on app shutdown"""
        db.disconnect()
    
    return app

if __name__ == '__main__':
    app = create_app()
    if app:
        print("🚀 Starting Investment Tracker API Server...")
        print(f"Environment: {FLASK_ENV}")
        app.run(debug=DEBUG, host='0.0.0.0', port=5000)
    else:
        print("Failed to start server")
