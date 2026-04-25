# 🚀 Smart Logistics - Render Deployment Guide

## Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- Render account (free tier available)
- Git repository configured

## Project Structure
```
Logistical_Distribution/
├── smart-logistics-backend/      # Node.js Express API
├── smart-logistics-frontend/     # Streamlit Dashboard
├── smart-logistics-ml/           # Python ML Engine
├── Procfile                      # Render process definition
├── render.yaml                   # Render deployment config
├── build.sh                      # Build script
└── start.sh                      # Startup script
```

## Local Development Setup

### 1. Install Dependencies
```bash
chmod +x build.sh
./build.sh
```

### 2. Create Environment Files
```bash
cp .env.example .env
cp smart-logistics-backend/.env.example smart-logistics-backend/.env
cp smart-logistics-frontend/.env.example smart-logistics-frontend/.env
```

### 3. Start Local Services

**Terminal 1 - Backend:**
```bash
cd smart-logistics-backend
npm install
npm run dev
# Backend runs on http://localhost:8000
```

**Terminal 2 - Dashboard:**
```bash
cd smart-logistics-frontend
pip install -r requirements.txt
streamlit run app.py
# Dashboard runs on http://localhost:8501
```

## Deployment to Render

### Step 1: Prepare Repository
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Services

#### Option A: Using Render Blueprint (render.yaml)
1. Go to https://render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Select `render.yaml`
5. Configure environment variables
6. Deploy

#### Option B: Manual Creation

**Backend Service:**
1. New + → Web Service
2. Connect GitHub repository
3. Settings:
   - Name: `smart-logistics-backend`
   - Region: Choose closest
   - Runtime: Node
   - Start Command: `npm run start:backend`
   - Environment:
     - NODE_ENV: production
     - PORT: 8000
     - PYTHON_EXECUTABLE: python3

**Dashboard Service:**
1. New + → Web Service
2. Connect GitHub repository
3. Settings:
   - Name: `smart-logistics-dashboard`
   - Region: Same as backend
   - Runtime: Python 3
   - Start Command: `streamlit run smart-logistics-frontend/app.py --server.port=$PORT --server.headless=true`
   - Environment:
     - STREAMLIT_SERVER_PORT: 3001
     - STREAMLIT_SERVER_HEADLESS: true

### Step 3: Environment Variables
Add to both services:
```
BACKEND_PORT=8000
NODE_ENV=production
PYTHON_EXECUTABLE=python3
ALLOWED_ORIGINS=https://your-dashboard-url.onrender.com,https://your-backend-url.onrender.com
RENDER_EXTERNAL_URL=https://your-backend-url.onrender.com
```

### Step 4: Monitor Deployment
1. Check Render Dashboard for deployment status
2. View logs in real-time
3. Test endpoints:
   - Backend: `https://your-backend-url.onrender.com/api/health`
   - Dashboard: `https://your-dashboard-url.onrender.com`

## Production Deployment Checklist

### Backend
- [x] Environment variables configured
- [x] CORS properly set for production URLs
- [x] Error handling implemented
- [x] Logging configured
- [x] Health check endpoint available
- [ ] Update ALLOWED_ORIGINS with actual Render URLs
- [ ] Add Firebase credentials if needed
- [ ] Configure any required API keys

### Frontend (Dashboard)
- [x] Map visualization optimized
- [x] State coordinates database complete
- [x] Dependencies in requirements.txt
- [ ] API endpoint updated to backend URL
- [ ] Analytics configured (optional)

### ML Engine
- [x] Dependencies in requirements.txt
- [x] Error handling for data processing
- [ ] Model files available
- [ ] Pre-trained models bundled if needed

## Troubleshooting

### Backend won't start
```bash
# Check logs
render logs smart-logistics-backend

# Common issues:
# - PORT not set: add PORT=8000 to env vars
# - Python not found: ensure Python 3 is in runtime
```

### Dashboard connection issues
```bash
# Check CORS configuration
# Update ALLOWED_ORIGINS in .env with actual deployed URLs
```

### Map not rendering
```bash
# Verify map_utils.py is in correct location
# Check Streamlit version: pip install --upgrade streamlit
```

## Scaling on Render

### Upgrade from Free to Pro
1. Go to service settings
2. Change plan from Free to Pro
3. Benefits:
   - Custom domains
   - SSL certificates
   - Better uptime SLA
   - Manual horizontal scaling

### Performance Tips
- Free tier: Cold starts expected (5-10s first request)
- Pro tier: Reserved capacity available
- Use caching in dashboard for frequent queries
- Optimize ML computations

## Custom Domain Setup
1. In Render Dashboard → Service Settings
2. Add custom domain
3. Point DNS records to Render
4. Wait for SSL certificate provisioning

## Monitoring & Analytics

### Check Service Health
```
GET /api/health
```

### View Real-time Logs
Dashboard → Service → Logs

### Monitor Resource Usage
Dashboard → Service → Metrics

## Costs Estimate (Free Tier)
- 2 Web Services: $0 (free tier)
- Free tier limitations:
  - Auto-sleep after 15 mins inactivity
  - Shared resources
  - 100GB bandwidth/month

## Next Steps
1. Deploy backend first
2. Test API endpoints
3. Deploy dashboard
4. Update API endpoint configuration
5. Test full integration
6. Monitor logs and fix issues
7. Consider upgrading services for production use

## Support
- Render Docs: https://render.com/docs
- GitHub Issues: Report bugs and feature requests
- Community: Join discussions for help
