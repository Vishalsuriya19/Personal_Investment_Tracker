@echo off
REM Investment Tracker Setup and Run Script for Windows
REM This script helps with installation and running the application

setlocal enabledelayedexpansion

echo.
echo =========================================
echo  AI Personal Investment Tracker
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

echo [1/6] Checking Python installation...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

echo.
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/6] Installing dependencies...
pip install -r requirements.txt

echo.
echo [5/6] Creating .env file from .env.example...
if not exist ".env" (
    copy .env.example .env
    echo .env file created. Please edit it with your database credentials.
) else (
    echo .env file already exists
)

echo.
echo [6/6] Training ML models...
python ml_models/train_model.py

echo.
echo =========================================
echo  Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database credentials
echo 2. Create MySQL database by running: mysql -u root -p^< database/schema.sql
echo 3. In Terminal 1, run: python backend/app.py
echo 4. In Terminal 2, run: streamlit run frontend/app.py
echo 5. Open http://localhost:8501 in your browser
echo.
echo =========================================
