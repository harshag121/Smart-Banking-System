@echo off
REM Fast API Banking Chatbot - Startup Script for Windows

echo 🏦 Banking Chatbot FastAPI Server
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    exit /b 1
)

REM Check if we're in the backend directory
if not exist "main.py" (
    echo ❌ main.py not found. Please run this script from the backend directory.
    exit /b 1
)

REM Install/update requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Dependencies installed!
echo.
echo 🚀 Starting FastAPI server...
echo API available at: http://localhost:8000
echo Docs available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the server
python main.py
