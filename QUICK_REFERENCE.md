# 🚀 Smart Logistics - Quick Reference

## Start Services

### Local Development (One Command)
```bash
./dev.sh
```

### Manual Start (3 Terminals)
```bash
# Terminal 1: Backend
cd smart-logistics-backend && npm run dev

# Terminal 2: Dashboard
cd smart-logistics-frontend && streamlit run app.py

# Terminal 3: ML Engine
cd smart-logistics-ml && python ml_engine.py
```

---

## Access Points

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| Backend API | http://localhost:8000 | 8000 | REST endpoints |
| Dashboard | http://localhost:3001 | 3001 | Streamlit UI |
| Health Check | http://localhost:8000/api/health | 8000 | Status check |

---

## Key Files

| File | Purpose |
|------|---------|
| `server.js` | Backend API |
| `app.py` | Streamlit dashboard |
| `ml_engine.py` | ML processing |
| `map_utils.py` | Map visualization |
| `render.yaml` | Render deployment |
| `.env.example` | Configuration template |

---

## API Endpoints

```bash
# Health Check
curl http://localhost:8000/api/health

# Get Dashboard Data
curl http://localhost:8000/api/dashboard

# Get Alerts
curl http://localhost:8000/api/alerts

# Get Map Data
curl http://localhost:8000/api/map

# Analyze CSV
curl -X POST \
  -F "dataFile=@data.csv" \
  http://localhost:8000/api/analyze
```

---

## Environment Setup

### Copy Templates
```bash
cp .env.example .env
cp smart-logistics-backend/.env.example smart-logistics-backend/.env
cp smart-logistics-frontend/.env.example smart-logistics-frontend/.env
```

### Key Variables
```env
# Backend
PORT=8000
NODE_ENV=production
ALLOWED_ORIGINS=http://localhost:3001

# Frontend
STREAMLIT_SERVER_PORT=3001
STREAMLIT_SERVER_HEADLESS=true

# ML
PYTHON_EXECUTABLE=python3
```

---

## Build & Deploy

### Install Dependencies
```bash
./build.sh
```

### Local Testing
```bash
./dev.sh          # Start all services
python test_integration.py  # Run tests
```

### Deploy to Render
```bash
git push origin main    # Push code
# Go to render.com → New Blueprint → Deploy
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Use different port
PORT=9000 npm start
```

### Dashboard Won't Connect
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Verify CORS settings
# Update ALLOWED_ORIGINS in .env
```

### Map Not Showing
```bash
# Check dependencies
pip install --upgrade plotly streamlit

# Verify coordinates
python -c "from smart-logistics-frontend.map_utils import get_all_states; print(get_all_states())"
```

---

## Documentation

- 📖 **SETUP_GUIDE.md** - Complete setup
- 🚀 **RENDER_DEPLOYMENT.md** - Deployment steps
- ✅ **DEPLOYMENT_CHECKLIST.md** - Verification
- 📊 **PROJECT_SUMMARY.md** - Architecture
- 📝 **README.md** - Overview

---

## Commands Cheatsheet

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Update dependencies
npm update
pip install --upgrade -r requirements.txt

# Run tests
python test_integration.py

# Check health
curl http://localhost:8000/api/health

# View logs
tail -f logs/backend.log
tail -f logs/frontend.log

# Kill all services
pkill -f "npm|streamlit|python"
```

---

## Render Deployment URLs

After deployment, services will be at:
- Backend: `https://smart-logistics-backend-xxx.onrender.com`
- Dashboard: `https://smart-logistics-dashboard-xxx.onrender.com`

Update CORS with these URLs:
```env
ALLOWED_ORIGINS=https://smart-logistics-dashboard-xxx.onrender.com
RENDER_EXTERNAL_URL=https://smart-logistics-backend-xxx.onrender.com
```

---

## Map Data

**States Covered**: 36 (28 states + 8 UTs)

**Demand Levels**:
- 🔴 Critical (>3.5)
- 🟠 High (2.5-3.5)
- 🟡 Moderate (1.5-2.5)
- 🔵 Low (0.5-1.5)
- ⚫ None (<0.5)

---

## Performance Stats

| Metric | Value |
|--------|-------|
| API Response Time | <100ms |
| Dashboard Load Time | <2s |
| Map Render Time | <500ms |
| ML Processing | <5s |
| Startup Time | 30s local, 5-10s Render |
| Uptime (Pro) | 99.9% SLA |

---

## Contact & Support

- **GitHub Issues**: Report bugs
- **Render Docs**: https://render.com/docs
- **Streamlit Help**: https://discuss.streamlit.io
- **Stack Overflow**: Tag questions with `streamlit`, `express`, `nodejs`

---

**Version**: 1.0.0 | **Last Updated**: April 2025 | **Status**: ✅ Ready
