#!/bin/bash

# Production startup script for Render deployment
set -e

echo "🚀 Starting Smart Logistics Application"
echo "=========================================================="

# Set production environment
export NODE_ENV=production
export PYTHON_EXECUTABLE=python3

# Get the port from environment or use default
PORT=${PORT:-8000}
STREAMLIT_PORT=${STREAMLIT_PORT:-3001}

echo "Backend port: $PORT"
echo "Dashboard port: $STREAMLIT_PORT"

# Create uploads directory if it doesn't exist
mkdir -p smart-logistics-backend/uploads

# Start backend server
echo "Starting backend server..."
cd smart-logistics-backend
npm start &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Python dashboard
echo "Starting Python dashboard..."
cd ../smart-logistics-frontend
streamlit run app.py --server.port=$STREAMLIT_PORT --server.headless=true &
FRONTEND_PID=$!

echo "✅ Application started!"
echo "Backend running on port $PORT"
echo "Dashboard running on port $STREAMLIT_PORT"

# Keep process alive
wait
