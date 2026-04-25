#!/bin/bash

# Local Development Startup Script
# Starts all services for local development

set -e

echo "🚀 Starting Smart Logistics Development Environment"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    kill $ML_PID 2>/dev/null || true
    echo -e "${GREEN}✅ All services stopped${NC}"
}

trap cleanup EXIT

# Create necessary directories
mkdir -p smart-logistics-backend/uploads
mkdir -p smart-logistics-frontend/data

# Start Backend
echo -e "${BLUE}Starting Backend Server...${NC}"
cd smart-logistics-backend
npm install > /dev/null 2>&1 || echo "Backend dependencies already installed"
npm run dev &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo -e "   API: ${BLUE}http://localhost:8000${NC}"
sleep 2

# Start Frontend
echo -e "${BLUE}Starting Dashboard...${NC}"
cd ../smart-logistics-frontend
pip install -q -r requirements.txt 2>/dev/null || echo "Dashboard dependencies already installed"
streamlit run app.py --server.port 3001 --logger.level=warning &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Dashboard started (PID: $FRONTEND_PID)${NC}"
echo -e "   Dashboard: ${BLUE}http://localhost:3001${NC}"

echo ""
echo "=========================================================="
echo -e "${GREEN}✅ All services are running!${NC}"
echo ""
echo "📊 Access Points:"
echo -e "  Backend API:    ${BLUE}http://localhost:8000${NC}"
echo -e "  Dashboard:      ${BLUE}http://localhost:3001${NC}"
echo -e "  Health Check:   ${BLUE}http://localhost:8000/api/health${NC}"
echo ""
echo "📝 View Logs:"
echo "  - Check terminal windows for real-time logs"
echo "  - Backend logs in left terminal"
echo "  - Dashboard logs in right terminal"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo "=========================================================="

# Keep script running
wait
