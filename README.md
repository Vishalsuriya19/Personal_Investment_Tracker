# Personal Investment Tracker
Personal Investment Tracker is a web-based AI-powered financial management application that analyzes an individual's income, expenses, savings, loans, and current investments to generate risk-aware investment recommendations.
The system uses machine learning models to predict future prices of commodities such as stocks, gold, and silver, and provides personalized guidance through an AI-generated report showing future investment plans and expected growth of current investments.
The application also includes an interactive dashboard to monitor savings, expenses, portfolio distribution, predictions, and investment recommendations.

## User Flows
Step 1 — User Registration / Login
User opens the web application.

Flow:
User enters username and password
If new user → Register account
If existing user → Login


Step 2 — Enter Personal Financial Details
User fills financial profile form.

Inputs:
Monthly income
Current savings
Current loans / EMI
Medical expenses
Food expenses
Transport expenses
Other expenses
Current investments (Gold / Stocks / Silver / Shares)

Purpose:
Understand financial condition
Calculate available investment amount
Calculate risk level

Output:
Financial profile stored in database

Step 3 — Risk Factor Calculation
System analyzes financial data.

Process:
Calculate total expenses
Calculate savings ratio
Check loan burden
Check emergency balance

Risk Levels:
Low Risk → Safe investor
Medium Risk → Balanced investor
High Risk → Aggressive investor

Output:
Risk score
Risk category

Used by:
Recommendation engine
AI report
Dashboard

Step 4 — Current Investment Analysis
System checks existing investments.

System calculates:
Total investment
Investment distribution
Growth potential

Purpose:
Understand portfolio balance
Detect over-risk / under-investment


System predicts future prices using ML.

Prediction for:
Gold price
Silver price
Stock price

Model used:
Regression
LSTM / Transformer
Ensemble model

Output:
Future price graph
Expected return %
Buy / Hold / Sell suggestion

Purpose:
Used for recommendation
Used for AI report

Step 6 — Investment Recommendation Engine
System generates recommendation based on:

Risk level
Savings
Market prediction
Current investments



Purpose:
Guide future investments

Step 7 — AI Report Generation
System generates financial guidance report.

Report includes:
User financial summary
Risk level
Current investment growth
Future prediction
Recommended investment plan
Expected portfolio growth


## Alternatives & Competition
1. INDmoney
Tracks stocks, mutual funds, EPF, US stocks
Shows net worth in one dashboard
Gives tax & profit insights
Popular in India (recommended)

2. Wealth Tracker
Focused on mutual fund investments
Easy SIP tracking
Good for beginners in India

3. Finary
Tracks all assets (stocks, crypto, real estate, bank accounts)
Real-time performance + analytics
Portfolio diversification insights
Supports multiple global platforms

## Stack 
Frontend : Streamlit
Streamlit can be used as the frontend UI because it allows you to build web dashboards using Python, which is very useful when the project contains machine learning, prediction, and data visualization.

Backend : Python Flask
Python Flask is used as the backend framework because the project requires integration of machine learning models, database operations, and API communication

ML Models : Scikit-learn + TensorFlow
Regression Models for predictions , NLP for AI report generation

Database : MySQL
MySQL is used as the database because the project requires reliable storage of user financial data, investment records, authentication details, and AI-generated reports. MySQL provides secure, structured, and efficient data management, which is suitable for a web-based financial tracking application.

Authentication : JWT (JSON Web Token)
JWT is a secure method to authenticate users by generating a token (digital key) after login, which is used to verify the user in future requests.
