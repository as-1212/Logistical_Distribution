# Smart Logistics - Complete Setup Guide

## 📋 Project Overview

This is a **Google Solution Challenge-level** full-stack AI-powered logistics platform with:
- **React/Streamlit Frontend**: Real-time dashboard with interactive India map
- **Node.js Backend**: Express API with Socket.io for real-time updates
- **Python ML Engine**: K-Means clustering for demand optimization

---

## 🚀 Quick Start (5 minutes)

### 1. Clone & Install
```bash
cd Logistical_Distribution
chmod +x build.sh dev.sh
./build.sh
```

### 2. Start Development
```bash
chmod +x dev.sh
./dev.sh
```

### 3. Access Services
- **Backend API**: http://localhost:8000
- **Dashboard**: http://localhost:3001
- **Health Check**: http://localhost:8000/api/health

---

## 📁 Project Structure

```
Logistical_Distribution/
│
├── smart-logistics-backend/          # Node.js + Express API
│   ├── server.js                     # Main server file
│   ├── package.json                  # Dependencies
│   ├── .env.example                  # Environment template
│   └── uploads/                      # File upload directory
│
├── smart-logistics-frontend/         # Streamlit Dashboard
│   ├── app.py                        # Main dashboard app
│   ├── dashboard.py                  # Dashboard components
│   ├── map_utils.py                  # Enhanced map visualization
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment template
│
├── smart-logistics-ml/               # Python ML Engine
│   ├── ml_engine.py                  # ML processing engine
│   └── requirements.txt              # Python dependencies
│
├── Procfile                          # Render deployment config
├── render.yaml                       # Render blueprint
├── build.sh                          # Build script
├── dev.sh                            # Development startup
├── start.sh                          # Production startup
├── test_integration.py               # Integration tests
└── RENDER_DEPLOYMENT.md              # Deployment guide
```

---

## 🔧 Backend Setup

### Install Dependencies
```bash
cd smart-logistics-backend
npm install
```

### Environment Variables
```bash
cp .env.example .env
```

**Configuration options:**
```
PORT=8000                              # API port
NODE_ENV=development                   # Environment
PYTHON_EXECUTABLE=python3              # Python path
ALLOWED_ORIGINS=http://localhost:3001  # CORS origins
```

### Start Backend
```bash
# Development (with auto-reload)
npm run dev

# Production
npm start
```

**API Endpoints:**
```
GET  /api/health              # Health check
GET  /api/dashboard           # Dashboard data
GET  /api/alerts              # Alert list
GET  /api/map                 # Map state data
POST /api/analyze             # Upload & analyze CSV
```

---

## 📊 Frontend Setup

### Install Dependencies
```bash
cd smart-logistics-frontend
pip install -r requirements.txt
```

### Environment Variables
```bash
cp .env.example .env
```

### Start Dashboard
```bash
streamlit run app.py

# Or specify port
streamlit run app.py --server.port 3001
```

**Features:**
- ✅ Real-time KPI cards
- ✅ Interactive India demand map
- ✅ Demand heatmap (State vs Product)
- ✅ Revenue and order trends
- ✅ AI insights panel
- ✅ Activity feed

---

## 🧠 ML Engine Setup

### Install Dependencies
```bash
cd smart-logistics-ml
pip install -r requirements.txt
```

### ML Pipeline
```python
from ml_engine import SmartLogisticsML

ml = SmartLogisticsML()
ml.load_data(data_input)
ml.preprocess_data()
results = ml.run_ai_analysis()
alerts = ml.generate_alerts()
```

**Processing Steps:**
1. Data loading & preprocessing
2. Demand scoring calculation
3. K-Means clustering (4 clusters)
4. Stock allocation optimization
5. Alert generation
6. Insight extraction

---

## 🗺️ Map Features

### Interactive India Map
- **Complete State Coverage**: All 28 states + 8 UTs
- **Accurate Coordinates**: Centroid-based positioning
- **Demand Visualization**: Size and color coding
- **Hover Information**: State details on hover

### Map Data Structure
```python
INDIA_STATE_COORDINATES = {
    'Andhra Pradesh': [15.9129, 79.7400],
    'Maharashtra': [19.7515, 75.7139],
    # ... 36 total states/UTs
}

# Demand Levels
- Critical (>3.5): Red (#EF4444)
- High (2.5-3.5): Orange (#F97316)
- Moderate (1.5-2.5): Amber (#F59E0B)
- Low (0.5-1.5): Blue (#60A5FA)
- None (<0.5): Gray (#D1D5DB)
```

---

## 🧪 Testing

### Integration Tests
```bash
# Start all services first
./dev.sh

# In another terminal
python test_integration.py
```

**Tests included:**
- ✅ Backend health check
- ✅ Dashboard API connectivity
- ✅ Alerts endpoint validation
- ✅ Map data availability
- ✅ CORS header configuration
- ✅ Error handling (404, 500)
- ✅ JSON content type

---

## 📦 Render Deployment

### Prerequisites
1. GitHub repository with code pushed
2. Render account (free tier available)
3. Environment variables configured

### Deploy Option 1: Using Blueprint (Recommended)
```bash
1. Go to https://render.com
2. Click "New +" → "Blueprint"
3. Select your GitHub repo
4. Choose render.yaml
5. Configure environment
6. Click "Deploy"
```

### Deploy Option 2: Manual Services
```
1. Create backend service
   - Runtime: Node
   - Start Command: npm run start:backend
   
2. Create dashboard service
   - Runtime: Python
   - Start Command: streamlit run smart-logistics-frontend/app.py
   
3. Add environment variables to both
```

### Environment Variables for Production
```
NODE_ENV=production
PORT=8000
ALLOWED_ORIGINS=https://your-dashboard.onrender.com,https://your-backend.onrender.com
RENDER_EXTERNAL_URL=https://your-backend.onrender.com
PYTHON_EXECUTABLE=python3
```

### Post-Deployment Checklist
- [ ] Backend health check passes
- [ ] Dashboard loads without errors
- [ ] Map renders correctly
- [ ] API calls return data
- [ ] CORS headers are set
- [ ] No console errors

---

## 🔐 Environment Variables

### Backend (.env)
```env
PORT=8000
NODE_ENV=production
PYTHON_EXECUTABLE=python3
ALLOWED_ORIGINS=http://localhost:3001
LOG_LEVEL=info
MAX_UPLOAD_SIZE=10485760
RENDER_EXTERNAL_URL=
```

### Frontend (.env)
```env
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_GEMINI_API_KEY=
```

### ML (.env)
```env
ML_ENGINE_PATH=ml_engine.py
PYTHON_EXECUTABLE=python3
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port is in use
lsof -i :8000

# Kill process
kill -9 <PID>

# Try different port
PORT=9000 npm start
```

### Dashboard connection error
```bash
# Verify API URL
curl http://localhost:8000/api/health

# Check CORS settings
# Update ALLOWED_ORIGINS in .env
```

### Map not rendering
```bash
# Verify dependencies
pip install --upgrade plotly streamlit

# Check browser console for errors
# Clear browser cache
```

### Python module not found
```bash
# Reinstall dependencies
pip install -r smart-logistics-frontend/requirements.txt
pip install -r smart-logistics-ml/requirements.txt
```

---

## 📈 Performance Tips

### Local Development
- Use `npm run dev` for hot-reload
- Keep browser DevTools open
- Monitor network tab for API calls

### Production (Render)
- Free tier: Expect 5-10s cold start
- Upgrade to Pro for better performance
- Enable caching for static data
- Optimize ML computations

---

## 🚀 Next Steps

1. **Customize Dashboard**
   - Add your company logo
   - Modify color scheme in CSS
   - Update product categories

2. **Integrate Real Data**
   - Connect to your database
   - Import actual inventory data
   - Set up data pipeline

3. **Extend ML Engine**
   - Train on historical data
   - Add forecasting models
   - Implement recommendations

4. **Add Authentication**
   - Implement login system
   - Add user roles
   - Secure API endpoints

5. **Deploy to Production**
   - Set up custom domain
   - Configure SSL certificates
   - Scale services as needed

---

## 📞 Support & Resources

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Express.js Docs**: https://expressjs.com
- **Scikit-learn Docs**: https://scikit-learn.org

---

## 📝 License

MIT License - Feel free to use, modify, and distribute

---

## 🎯 Key Metrics

| Metric | Value |
|--------|-------|
| States Covered | 28 + 8 UTs (Complete India) |
| API Endpoints | 4 main + analytics |
| Real-time Updates | Socket.io enabled |
| ML Models | K-Means clustering |
| Deployment | Render-ready |
| Startup Time | < 30s (local), 5-10s cold start (Render) |

---

**Last Updated**: April 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
