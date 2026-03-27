"""
API routes for Investment Tracker
"""
from flask import Blueprint, request, jsonify
from functools import wraps
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))
from backend.auth import AuthHandler
from backend.jwt_utils import JWTHandler
from backend.db import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

def token_required(f):
    """Decorator to check if valid JWT token is provided"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Extract token from headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        payload = JWTHandler.verify_token(token)
        if not payload:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        return f(payload, *args, **kwargs)
    
    return decorated_function

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@api_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        success, message = AuthHandler.register_user(name, email, password)
        
        if success:
            return jsonify({'success': True, 'message': message}), 201
        else:
            return jsonify({'success': False, 'message': message}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        success, token, message = AuthHandler.login_user(email, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'token': token
            }), 200
        else:
            return jsonify({'success': False, 'message': message}), 401
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ============================================================================
# PORTFOLIO ROUTES
# ============================================================================

@api_bp.route('/portfolio', methods=['GET'])
@token_required
def get_portfolio(payload):
    """Get user's investment portfolio"""
    try:
        user_id = payload.get('user_id')
        
        investments = db.execute_query(
            """SELECT id, stock_name, quantity, purchase_price, amount, date 
               FROM investments WHERE user_id = %s ORDER BY date DESC""",
            (user_id,)
        )
        
        if investments:
            total_invested = sum(inv['amount'] for inv in investments)
            return jsonify({
                'success': True,
                'portfolio': investments,
                'total_invested': float(total_invested)
            }), 200
        else:
            return jsonify({
                'success': True,
                'portfolio': [],
                'total_invested': 0
            }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/add_investment', methods=['POST'])
@token_required
def add_investment(payload):
    """Add a new investment"""
    try:
        user_id = payload.get('user_id')
        data = request.get_json()
        
        stock_name = data.get('stock_name')
        quantity = data.get('quantity', 1)
        purchase_price = data.get('purchase_price')
        date = data.get('date')
        
        amount = float(quantity) * float(purchase_price)
        
        investment_id = db.execute_insert(
            """INSERT INTO investments 
               (user_id, stock_name, quantity, purchase_price, amount, date) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, stock_name, quantity, purchase_price, amount, date)
        )
        
        if investment_id:
            return jsonify({
                'success': True,
                'message': 'Investment added successfully',
                'investment_id': investment_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Error adding investment'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ============================================================================
# PREDICTION ROUTES
# ============================================================================

@api_bp.route('/predict', methods=['POST'])
@token_required
def predict(payload):
    """Get predictions for investments"""
    try:
        user_id = payload.get('user_id')
        
        # This will be integrated with ML model later
        predictions = db.execute_query(
            """SELECT stock_name, current_price, predicted_price, risk_level, 
                      profit_probability FROM predictions WHERE user_id = %s 
               ORDER BY date DESC LIMIT 10""",
            (user_id,)
        )
        
        return jsonify({
            'success': True,
            'predictions': predictions if predictions else []
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ============================================================================
# REPORT ROUTES
# ============================================================================

@api_bp.route('/report', methods=['GET'])
@token_required
def get_report(payload):
    """Get AI-generated report"""
    try:
        user_id = payload.get('user_id')
        
        # Get latest report
        report = db.execute_query(
            """SELECT report_text, risk_assessment, recommendations, date 
               FROM reports WHERE user_id = %s ORDER BY date DESC LIMIT 1""",
            (user_id,)
        )
        
        if report:
            return jsonify({
                'success': True,
                'report': report[0]
            }), 200
        else:
            return jsonify({
                'success': True,
                'report': None,
                'message': 'No report generated yet'
            }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@api_bp.route('/generate_report', methods=['POST'])
@token_required
def generate_report(payload):
    """Generate AI report - endpoint for ML/NLP service"""
    try:
        user_id = payload.get('user_id')
        data = request.get_json()
        
        report_text = data.get('report_text')
        risk_assessment = data.get('risk_assessment')
        recommendations = data.get('recommendations')
        date = data.get('date')
        
        report_id = db.execute_insert(
            """INSERT INTO reports 
               (user_id, report_text, risk_assessment, recommendations, date) 
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, report_text, risk_assessment, recommendations, date)
        )
        
        if report_id:
            return jsonify({
                'success': True,
                'message': 'Report generated successfully',
                'report_id': report_id
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Error generating report'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ============================================================================
# HEALTH CHECK
# ============================================================================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Investment Tracker API'}), 200
