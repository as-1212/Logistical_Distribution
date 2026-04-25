# Deployment Checklist

## Pre-Deployment ✅

### Code Quality
- [x] No console.log in production code
- [x] Error handling implemented
- [x] CORS properly configured
- [x] Environment variables documented
- [x] Dependencies pinned to versions

### Security
- [x] Helmet.js enabled for security headers
- [x] CORS whitelist configured
- [x] Input validation implemented
- [x] No hardcoded secrets in code
- [ ] API rate limiting configured (optional)
- [ ] HTTPS enforced (automatic on Render)

### Frontend
- [x] Map visualization working
- [x] All dependencies in requirements.txt
- [x] No localhost references
- [x] Responsive design tested
- [ ] Performance optimized

### Backend
- [x] Health check endpoint working
- [x] All API routes tested
- [x] Error responses formatted
- [x] Logging configured
- [x] CORS headers added

### ML Engine
- [x] Dependencies frozen
- [x] Error handling for bad data
- [x] No file system writes to uploads
- [ ] Performance tested with large datasets

---

## Deployment Preparation

### Environment Setup
```bash
# 1. Copy environment templates
cp .env.example .env
cp smart-logistics-backend/.env.example smart-logistics-backend/.env
cp smart-logistics-frontend/.env.example smart-logistics-frontend/.env

# 2. Update with Render URLs (after deployment)
# RENDER_EXTERNAL_URL=https://backend-url.onrender.com
# ALLOWED_ORIGINS=https://dashboard-url.onrender.com
```

### Repository Cleanup
```bash
# 1. Remove local env files with secrets
rm smart-logistics-backend/.env
rm smart-logistics-frontend/.env

# 2. Ensure .gitignore includes:
echo ".env" >> .gitignore
echo "uploads/" >> .gitignore
echo "node_modules/" >> .gitignore
echo "__pycache__/" >> .gitignore

# 3. Commit changes
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Render Deployment Steps

### Step 1: Create Backend Service
```
Service Name: smart-logistics-backend
Runtime: Node
Build Command: npm install
Start Command: npm run start:backend
Environment Variables:
  - NODE_ENV: production
  - PORT: 8000
  - PYTHON_EXECUTABLE: python3
```

### Step 2: Create Dashboard Service
```
Service Name: smart-logistics-dashboard
Runtime: Python
Build Command: pip install -r smart-logistics-frontend/requirements.txt
Start Command: streamlit run smart-logistics-frontend/app.py --server.port=$PORT --server.headless=true
Environment Variables:
  - STREAMLIT_SERVER_HEADLESS: true
  - PORT: 3000
```

### Step 3: Update CORS Configuration
After services are deployed:
```
# Get the deployed URLs from Render
Backend URL: https://smart-logistics-backend-xxx.onrender.com
Dashboard URL: https://smart-logistics-dashboard-xxx.onrender.com

# Update environment variables
Backend:
  ALLOWED_ORIGINS=https://smart-logistics-dashboard-xxx.onrender.com,https://smart-logistics-backend-xxx.onrender.com
  RENDER_EXTERNAL_URL=https://smart-logistics-backend-xxx.onrender.com

Dashboard:
  BACKEND_API_URL=https://smart-logistics-backend-xxx.onrender.com
```

---

## Post-Deployment Verification

### Test Backend
```bash
# Health check
curl https://your-backend-url.onrender.com/api/health

# Dashboard data
curl https://your-backend-url.onrender.com/api/dashboard

# Map data
curl https://your-backend-url.onrender.com/api/map
```

### Test Dashboard
- [ ] Dashboard loads without errors
- [ ] Map renders correctly with all states
- [ ] KPI cards display data
- [ ] Charts load and refresh
- [ ] No 404 errors in console

### Monitor Logs
```
# Backend logs
Dashboard → smart-logistics-backend → Logs

# Dashboard logs
Dashboard → smart-logistics-dashboard → Logs

# Check for errors related to:
- CORS issues
- Missing environment variables
- Module import errors
- Connection timeouts
```

---

## Production Optimization

### Performance
- [ ] Enable gzip compression
- [ ] Cache static assets
- [ ] Optimize map rendering
- [ ] Minify frontend code
- [ ] Use CDN for static files (optional)

### Monitoring
- [ ] Set up error tracking (Sentry optional)
- [ ] Monitor resource usage
- [ ] Track API response times
- [ ] Set up alerts for failures

### Scaling
- [ ] Upgrade from free to Pro tier if needed
- [ ] Configure auto-restart
- [ ] Set up database backups
- [ ] Plan for traffic spikes

---

## Troubleshooting Checklist

| Issue | Solution |
|-------|----------|
| Backend won't start | Check PORT env var, verify Node modules installed |
| Dashboard connection error | Verify ALLOWED_ORIGINS includes dashboard URL |
| Map not rendering | Check browser console, verify plotly installed |
| Slow startup | Normal for free tier, consider Pro tier |
| 404 API errors | Check backend deployment status, verify endpoints |
| CORS errors | Update ALLOWED_ORIGINS with correct URLs |
| Module not found | Reinstall dependencies, check requirements.txt |
| Blank dashboard | Check network tab, verify API responses |

---

## Rollback Plan

### If Deployment Fails
```bash
# 1. Check service logs for errors
# 2. Verify environment variables are set
# 3. Ensure all files were deployed
# 4. Check build logs for dependency issues

# If critical issue:
# 1. Delete failed services
# 2. Fix code locally
# 3. Push to repository
# 4. Redeploy
```

---

## Documentation

- [ ] SETUP_GUIDE.md completed
- [ ] RENDER_DEPLOYMENT.md reviewed
- [ ] API endpoints documented
- [ ] Environment variables documented
- [ ] Troubleshooting guide updated
- [ ] Team has access to deployment credentials

---

## Final Sign-Off

- **Deployed By**: ___________________
- **Date**: ___________________
- **Backend URL**: ___________________
- **Dashboard URL**: ___________________
- **Status**: ✅ Ready for Production

---

**Last Updated**: April 2025
**Version**: 1.0.0
