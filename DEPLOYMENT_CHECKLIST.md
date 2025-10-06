# 🚀 Quick Start Deployment Checklist

## ✅ What I've Done For You

1. ✅ Pushed all code to GitHub: https://github.com/MuhammadSaif700/Medadhere
2. ✅ Created `frontend/config.js` - Auto-detects environment (local vs production)
3. ✅ Updated `frontend/index.html` - Uses config for API URL
4. ✅ Created comprehensive deployment guide: `AZURE_PORTAL_DEPLOYMENT.md`

---

## 📋 Your TODO List

### Part 1: Deploy Backend to Azure (15 minutes)

1. [ ] Go to https://portal.azure.com
2. [ ] Create new **Web App**:
   - Name: `medadhere-backend`
   - Runtime: Python 3.11
   - OS: Linux
   - Plan: Basic B1 (or Free F1)
3. [ ] Connect GitHub:
   - Deployment Center → GitHub
   - Select: `MuhammadSaif700/Medadhere`
   - Branch: `main`
   - Build Provider: GitHub Actions
4. [ ] Configure Settings:
   - Startup Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.main:app --bind 0.0.0.0:8000 --timeout 120`
   - Environment Variables:
     - `PYTHONPATH` = `/home/site/wwwroot`
     - `WEBSITES_PORT` = `8000`
     - `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
     - `ENABLE_ORYX_BUILD` = `true`
   - CORS: Allow `*` (temporarily)
5. [ ] Test Backend:
   - Visit: `https://medadhere-backend.azurewebsites.net/docs`
   - Verify Swagger UI loads
   - Test `/health` endpoint

### Part 2: Deploy Frontend to Netlify (10 minutes)

1. [ ] Go to https://netlify.com
2. [ ] Sign in with GitHub
3. [ ] Create new site:
   - Import from GitHub
   - Select: `MuhammadSaif700/Medadhere`
   - Base directory: `frontend`
   - Build command: (leave empty)
   - Publish directory: `frontend`
4. [ ] Deploy and get URL (e.g., `https://medadhere.netlify.app`)
5. [ ] Update Azure CORS:
   - Remove `*`
   - Add your Netlify URL

### Part 3: Verify Everything Works (5 minutes)

1. [ ] Open Netlify URL
2. [ ] Test Dashboard - should load stats
3. [ ] Test Pill Database - search should work
4. [ ] Test Identify Pill - image upload should work
5. [ ] Check browser console (F12):
   - Should see: "API Configuration: Production"
   - No CORS errors

---

## 📄 Detailed Instructions

Read the complete step-by-step guide in:
**`AZURE_PORTAL_DEPLOYMENT.md`**

This file has:
- Screenshots descriptions
- Troubleshooting tips
- Configuration examples
- Testing procedures

---

## 🎯 Expected URLs After Deployment

### Backend (Azure)
```
Main API: https://medadhere-backend.azurewebsites.net
API Docs: https://medadhere-backend.azurewebsites.net/docs
Health: https://medadhere-backend.azurewebsites.net/health
```

### Frontend (Netlify)
```
App: https://medadhere.netlify.app
(or https://<your-custom-name>.netlify.app)
```

---

## 🆘 Quick Help

### Backend Not Working?
1. Check Azure Log Stream (Monitoring → Log stream)
2. Verify GitHub Actions completed successfully
3. Ensure `requirements.txt` includes `gunicorn`

### Frontend Not Connecting?
1. Press F12 → Check Console for errors
2. Verify backend URL in Network tab
3. Check CORS is configured in Azure

### Need More Help?
- Read `AZURE_PORTAL_DEPLOYMENT.md` - Section 8: Troubleshooting
- Check Azure Activity Log
- Review Netlify deploy logs

---

## 💰 Cost Estimate

**Option 1: Free Tier**
- Azure F1: FREE (60 min/day limit)
- Netlify: FREE (100GB bandwidth)
- **Total: $0/month**

**Option 2: Production Ready**
- Azure B1: ~$13/month
- Netlify: FREE
- **Total: ~$13/month**

---

## ⏱️ Time Estimate

- Azure Setup: 15 minutes
- Netlify Setup: 10 minutes  
- Testing & Verification: 5 minutes
- **Total: ~30 minutes**

---

## 🎉 Ready to Deploy!

Open `AZURE_PORTAL_DEPLOYMENT.md` and follow the steps!

Good luck! 🚀
