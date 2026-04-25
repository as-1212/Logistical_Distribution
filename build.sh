#!/bin/bash

set -e

echo "🚀 Building Smart Logistics Application for Production"
echo "=========================================================="

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Build Backend
echo "📦 Installing backend dependencies..."
cd smart-logistics-backend
npm install
if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed"
else
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

# Build Frontend
echo "⚛️ Installing frontend dependencies..."
cd ../smart-logistics-frontend
npm install
if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

# Install Python ML dependencies
echo "🐍 Installing Python ML dependencies..."
cd ../smart-logistics-ml
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Python ML dependencies installed"
else
    echo "❌ Failed to install Python ML dependencies"
    exit 1
fi

echo ""
echo "✅ Build completed successfully!"
echo "Ready for deployment to Render"
