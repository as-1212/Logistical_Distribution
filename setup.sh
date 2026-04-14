#!/bin/bash

echo "🚀 Setting up Smart Resource Allocation AI for Retail Logistics"
echo "=========================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd smart-logistics-backend
npm install
if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed"
else
    echo "❌ Failed to install backend dependencies"
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

# Install frontend dependencies
echo "⚛️ Installing frontend dependencies..."
cd ../smart-logistics-frontend
npm install
if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "1. Start backend: cd smart-logistics-backend && npm start"
echo "2. Start frontend: cd smart-logistics-frontend && npm run dev"
echo "3. Open browser: http://localhost:3000"
echo ""
echo "📊 Backend runs on: http://localhost:5000"
echo "🌐 Frontend runs on: http://localhost:3000"
echo ""
echo "📖 For detailed instructions, see README.md"
