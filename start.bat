@echo off
echo ========================================
echo   Catalyst Talent Agent - Setup
echo ========================================
echo.
echo [1/2] Installing Python dependencies...
cd backend
pip install -r requirements.txt
echo.
echo [2/2] Starting backend server...
echo.
echo ========================================
echo   Backend running at http://localhost:8000
echo   Open frontend/index.html in your browser
echo ========================================
echo.
python main.py
