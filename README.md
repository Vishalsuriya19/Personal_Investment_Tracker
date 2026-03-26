# 📈 AI Personal Investment Tracker

A production-grade web application for managing investments with AI-powered predictions and portfolio analysis.

## 🎯 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Portfolio Management**: Add and manage investments
- **ML Predictions**: AI-powered price predictions and risk scoring
- **NLP Report Generation**: Automated AI-based portfolio analysis
- **Data Visualization**: Interactive charts and dashboard
- **MySQL Database**: Persistent data storage
- **RESTful API**: Flask backend with clean architecture

## 🏗️ Architecture

```
Frontend (Streamlit)
    ↓
Backend API (Flask)
    ↓
ML Models (Scikit-learn)
    ↓
Database (MySQL)
```

## 📁 Project Structure

```
investment_tracker/
├── frontend/
│   ├── app.py              # Streamlit UI
│   └── __init__.py
├── backend/
│   ├── app.py              # Flask application
│   ├── routes.py           # API endpoints
│   ├── auth.py             # Authentication logic
│   ├── jwt_utils.py        # JWT token handling
│   ├── db.py               # Database connection
│   └── __init__.py
├── ml_models/
│   ├── train_model.py      # Model training
│   ├── predict.py          # Prediction service
│   ├── nlp_report.py       # Report generation
│   └── __init__.py
├── database/
│   └── schema.sql          # Database schema
├── config.py               # Configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Git

### Installation

1. **Clone/Setup Project**
```bash
cd investment_tracker
```

2. **Create Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Create Database**

Connect to MySQL and run:
```bash
mysql -u root -p < database/schema.sql
```

Or create database manually:
```bash
mysql -u root -p
CREATE DATABASE investment_tracker;
USE investment_tracker;
# Then paste contents of database/schema.sql
```

5. **Configure Environment**

Create `.env` file in root directory:
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=investment_tracker
DB_PORT=3306

# Flask
FLASK_SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_PORT=5000

# JWT
JWT_SECRET_KEY=your-jwt-secret

# API
API_BASE_URL=http://localhost:5000
```

### Running the Application

**Terminal 1 - Start Backend API:**
```bash
python backend/app.py
```
API will run on `http://localhost:5000`

**Terminal 2 - Train ML Models:**
```bash
python ml_models/train_model.py
```

**Terminal 3 - Start Frontend:**
```bash
streamlit run frontend/app.py
```
UI will open at `http://localhost:8501`

## 📚 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login and get JWT token

### Portfolio
- `GET /api/portfolio` - Get user's investments
- `POST /api/add_investment` - Add new investment

### Predictions
- `POST /api/predict` - Generate predictions

### Reports
- `GET /api/report` - Get latest report
- `POST /api/generate_report` - Generate new report

### Health
- `GET /api/health` - API health check

## 🔐 Authentication

All protected endpoints require JWT token in header:
```bash
Authorization: Bearer <your_jwt_token>
```

## 🤖 Machine Learning Models

### Price Prediction (Regression)
- Uses RandomForest or GradientBoosting
- Predicts 30-day price outlook
- Features: days_held, market_sentiment, volatility, volume, RSI

### Risk Scoring
- Analyzes portfolio concentration
- Calculates overall risk level (Low/Medium/High)
- Provides risk score 0-100

### NLP Report Generation
- Generates insights from predictions
- Provides actionable recommendations
- Includes portfolio summary and outlook

## 📊 Database Schema

### users
- id, name, email, password_hash, timestamps

### investments
- id, user_id, stock_name, quantity, purchase_price, amount, date, timestamp

### predictions
- id, user_id, stock_name, current_price, predicted_price, risk_level, profit_probability, date

### reports
- id, user_id, report_text, risk_assessment, recommendations, date, timestamp

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Register User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"SecurePass123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"SecurePass123"}'
```

## 📈 Usage Flow

1. **Register/Login** - Create account or login
2. **Add Investments** - Input your stock holdings
3. **View Dashboard** - See portfolio summary
4. **Generate Predictions** - Get AI price forecasts
5. **Review Report** - Read AI-generated analysis
6. **Make Decisions** - Use insights for portfolio management

## ⚙️ Configuration

Edit `config.py` to customize:
- Database credentials
- JWT settings
- API URLs
- ML model parameters
- Application ports

## 🐛 Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check credentials in config.py or .env
- Verify database exists

### API Connection Error (from Streamlit)
- Check if Flask backend is running
- Verify API_BASE_URL in config.py
- Check CORS settings

### ML Model Issues
- Run `python ml_models/train_model.py` to retrain
- Check pickle files exist in ml_models/

## 📝 Development Notes

- Keep backend and frontend separate for scalability
- ML models can be retrained independently
- Database schema supports future extensions
- JWT tokens expire after 24 hours (configurable)
- All passwords are hashed using Werkzeug

## 🔒 Security Features

- Password hashing with Werkzeug
- JWT-based authentication
- Input validation on all endpoints
- CORS enabled for frontend communication
- SQL injection protection via parameterized queries

## 📦 Dependencies

Key packages:
- Flask 2.3.3 - Backend framework
- Streamlit 1.27.0 - Frontend framework
- MySQL Connector Python - Database
- Scikit-learn 1.3.0 - ML models
- PyJWT 2.8.1 - Authentication

## 🚀 Deployment

For production:
1. Use environment variables for sensitive data
2. Set `FLASK_ENV=production`
3. Use WSGI server (gunicorn, uWSGI)
4. Enable HTTPS
5. Use managed database service
6. Implement proper logging and monitoring

## 📄 License

MIT License

## 👨‍💼 About

Built as a comprehensive example of modern full-stack application architecture combining:
- Web framework (Flask)
- UI framework (Streamlit)
- Machine Learning (Scikit-learn)
- Database (MySQL)
- Authentication (JWT)

## 📞 Support

For issues or questions, refer to documentation in code comments.

---

**Happy Investing! 🚀📈**
