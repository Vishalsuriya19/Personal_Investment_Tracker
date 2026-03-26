# QUICK START GUIDE

## ⚡ 5-Minute Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+

### Step 1: Setup Environment
```bash
cd investment_tracker

# Windows
python -m venv venv
venv\Scripts\activate.bat

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Packages & Setup
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Step 3: Setup Database
```bash
# Create database
mysql -u root -p < database/schema.sql

# Edit .env with correct database credentials
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
```

### Step 4: Train ML Models
```bash
python ml_models/train_model.py
```

### Step 5: Start Services (Open 3 Terminals)

**Terminal 1: Start Flask Backend**
```bash
python backend/app.py
# Backend runs on http://localhost:5000
```

**Terminal 2: Start Streamlit Frontend**
```bash
streamlit run frontend/app.py
# UI opens at http://localhost:8501
```

**Terminal 3 (Optional): Run Tests**
```bash
pytest tests/ -v
```

---

## 🎯 First Time Usage

1. **Open browser** → http://localhost:8501
2. **Register** → Create account with email/password
3. **Login** → Use your credentials
4. **Add Investment** → Add your first stock holding
5. **View Dashboard** → See portfolio summary
6. **Generate Predictions** → Get AI predictions
7. **View Report** → Read AI analysis

---

## 📁 Project Files Overview

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask API server |
| `frontend/app.py` | Streamlit UI |
| `ml_models/train_model.py` | ML model training |
| `ml_models/predict.py` | Making predictions |
| `database/schema.sql` | Database tables |
| `config.py` | Configuration settings |
| `.env` | Environment variables |

---

## 🔧 Common Commands

```bash
# Train/retrain ML models
python ml_models/train_model.py

# Run tests
pytest tests/ -v

# Check API health
curl http://localhost:5000/api/health

# Reset database
mysql -u root -p investment_tracker < database/schema.sql
```

---

## 📞 Support

**Issue**: Database connection fails
- Check MySQL is running
- Verify .env credentials
- Ensure database exists

**Issue**: API connection error (Streamlit)
- Check Flask backend is running on port 5000
- Verify API_BASE_URL in config.py
- Try: `curl http://localhost:5000/api/health`

**Issue**: Streamlit not loading
- Clear cache: `streamlit cache clear`
- Ensure frontend/app.py exists
- Check Python path is correct

---

## 🚀 Next Steps

1. Add more stock data
2. Explore ML predictions
3. Customize risk assessment
4. Deploy to production
5. Extend with more features

For complete documentation, see DOCUMENTATION.md

**Happy Investing! 📈**
