::Quick setup script for Windows

@echo off
echo ======================================
echo STRESS DETECTION - SETUP SCRIPT
echo ======================================

:: Check Python
echo Checking Python...
python --version >nul 2>&1 || (echo Python not found & exit /b 1)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

:: Install Node dependencies
echo Installing Node dependencies...
cd client
npm install --legacy-peer-deps
cd ..

:: Create .env file
echo Creating .env file...
copy server\.env.example server\.env

echo.
echo ======================================
echo SETUP COMPLETE!
echo ======================================
echo.
echo To start development:
echo.
echo Terminal 1 (Backend):
echo   venv\Scripts\activate
echo   cd server ^&^& python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd client ^&^& npm start
echo.
echo API: http://localhost:5000
echo UI:  http://localhost:3000
