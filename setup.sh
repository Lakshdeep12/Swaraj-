#!/bin/bash

# Quick setup script for Linux/macOS

echo "======================================"
echo "STRESS DETECTION - SETUP SCRIPT"
echo "======================================"

# Check Python
echo "Checking Python..."
python3 --version || { echo "Python 3 not found"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node dependencies
echo "Installing Node dependencies..."
cd client
npm install --legacy-peer-deps
cd ..

# Create .env file
echo "Creating .env file..."
cp server/.env.example server/.env

echo ""
echo "======================================"
echo "SETUP COMPLETE!"
echo "======================================"
echo ""
echo "To start development:"
echo ""
echo "Terminal 1 (Backend):"
echo "  source venv/bin/activate"
echo "  cd server && python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd client && npm start"
echo ""
echo "API: http://localhost:5000"
echo "UI:  http://localhost:3000"
