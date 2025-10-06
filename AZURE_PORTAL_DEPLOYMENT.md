# 🚀 Deploy MedAdhere Backend to Azure Portal (Manual Guide)

## ✅ Prerequisites Checklist

- [x] GitHub repository: https://github.com/MuhammadSaif700/Medadhere
- [x] Azure account (free tier works)
- [x] Code pushed to GitHub
- [ ] Azure Portal access

---

## 📋 Part 1: Create Azure Web App Using Portal

### Step 1: Go to Azure Portal

1. Open your browser and go to: https://portal.azure.com
2. Sign in with your Microsoft account

### Step 2: Create a Web App

1. Click **"Create a resource"** (top-left or center)
2. Search for **"Web App"**
3. Click **"Create"** → **"Web App"**

### Step 3: Configure Basic Settings

Fill in the **"Basics"** tab:

| Field | Value |
|-------|-------|
| **Subscription** | Select your subscription |
| **Resource Group** | Create new: `medadhere-rg` |
| **Name** | `medadhere-backend` (must be globally unique) |
| **Publish** | ✅ **Code** |
| **Runtime stack** | **Python 3.11** |
| **Operating System** | **Linux** |
| **Region** | `East US` (or nearest to you) |

### Step 4: Configure App Service Plan

In the **"Pricing plans"** section:

1. Click **"Create new"** under Linux Plan
2. Name: `medadhere-plan`
3. Click **"Explore pricing plans"**
4. Select **"Basic B1"** (or Free F1 for testing)
   - B1: ~$13/month, better performance
   - F1: Free, limited resources
5. Click **"Select"**

### Step 5: Review and Create

1. Click **"Review + create"**
2. Review all settings
3. Click **"Create"**
4. Wait 1-2 minutes for deployment to complete
5. Click **"Go to resource"**

---

## 📋 Part 2: Connect GitHub Repository

### Step 6: Configure Deployment Center

1. In your Web App page, find **"Deployment"** section in left menu
2. Click **"Deployment Center"**

### Step 7: Select GitHub as Source

1. **Source**: Select **"GitHub"**
2. Click **"Authorize"** if needed (sign in to GitHub)
3. After authorization:
   - **Organization**: `MuhammadSaif700`
   - **Repository**: `Medadhere`
   - **Branch**: `main`

### Step 8: Configure Build Settings

1. **Build Provider**: Select **"GitHub Actions"** (recommended)
2. **Runtime Stack**: `Python 3.11`
3. Click **"Save"** at the top

✅ This will automatically:
- Create a GitHub Actions workflow file
- Add it to your repository (`.github/workflows/`)
- Trigger the first deployment

---

## 📋 Part 3: Configure Application Settings

### Step 9: Add Environment Variables

1. In left menu, go to **"Settings"** → **"Configuration"**
2. Click **"Application settings"** tab
3. Click **"+ New application setting"** for each:

| Name | Value |
|------|-------|
| `PYTHONPATH` | `/home/site/wwwroot` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |
| `WEBSITES_PORT` | `8000` |
| `ENABLE_ORYX_BUILD` | `true` |

4. Click **"Save"** at the top
5. Click **"Continue"** when prompted (app will restart)

### Step 10: Configure Startup Command

1. Still in **"Configuration"**
2. Click **"General settings"** tab
3. Find **"Startup Command"** field
4. Enter:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.main:app --bind 0.0.0.0:8000 --timeout 120
   ```
5. Click **"Save"** at the top

### Step 11: Enable CORS

1. In left menu, go to **"API"** → **"CORS"**
2. In **"Allowed Origins"**, add:
   - `*` (for now - we'll update with Netlify URL later)
3. Check ✅ **"Enable Access-Control-Allow-Credentials"**
4. Click **"Save"**

---

## 📋 Part 4: Monitor Deployment

### Step 12: Check Deployment Status

1. Go back to **"Deployment"** → **"Deployment Center"**
2. Click **"Logs"** tab
3. You'll see GitHub Actions workflow running
4. Click on the latest run to see details

**Expected steps:**
- ✅ Build job
- ✅ Deploy job
- ✅ Application started

### Step 13: View Application Logs

1. In left menu, go to **"Monitoring"** → **"Log stream"**
2. Wait for logs to appear
3. You should see:
   ```
   Starting gunicorn...
   Uvicorn running on http://0.0.0.0:8000
   Application startup complete
   ```

---

## 📋 Part 5: Test Your Deployment

### Step 14: Get Your Backend URL

1. In **"Overview"** page (main page of your Web App)
2. Find **"Default domain"**: `medadhere-backend.azurewebsites.net`
3. Copy this URL

### Step 15: Test Endpoints

Open these URLs in your browser:

1. **Health Check**: 
   ```
   https://medadhere-backend.azurewebsites.net/health
   ```
   ✅ Should return: `{"status":"healthy","service":"MedAdhere API"}`

2. **API Documentation**:
   ```
   https://medadhere-backend.azurewebsites.net/docs
   ```
   ✅ Should show Swagger UI with all endpoints

3. **Root Endpoint**:
   ```
   https://medadhere-backend.azurewebsites.net/
   ```
   ✅ Should return: `{"message":"Welcome to MedAdhere API","version":"1.0.0"}`

---

## 🎨 Part 6: Frontend Configuration Complete

### ✅ Step 16: Frontend Already Configured!

Great news! I've already updated your frontend to automatically detect the environment:

- **Local Development**: Uses `http://localhost:8010`
- **Production**: Uses `https://medadhere-backend.azurewebsites.net`

Files updated:
1. ✅ `frontend/config.js` - Created with auto-detection
2. ✅ `frontend/index.html` - Updated to use config

---

## 📋 Part 7: Deploy Frontend to Netlify

### Step 17: Sign Up / Sign In to Netlify

1. Go to: https://netlify.com
2. Click **"Sign up"** or **"Log in"**
3. Choose **"Sign up with GitHub"** (easiest)
4. Authorize Netlify to access your GitHub

### Step 18: Create New Site from Git

1. Click **"Add new site"** → **"Import an existing project"**
2. Click **"Deploy with GitHub"**
3. Find and select: **`MuhammadSaif700/Medadhere`**
4. Click on the repository

### Step 19: Configure Build Settings

| Field | Value |
|-------|-------|
| **Base directory** | `frontend` |
| **Build command** | (leave empty or type: `echo "No build"`) |
| **Publish directory** | `frontend` |
| **Branch to deploy** | `main` |

### Step 20: Add Environment Variables (Optional)

If you want to explicitly set the backend URL:

1. Click **"Show advanced"**
2. Click **"New variable"**
   - **Key**: `BACKEND_URL`
   - **Value**: `https://medadhere-backend.azurewebsites.net`

### Step 21: Deploy Site

1. Click **"Deploy site"**
2. Wait 1-2 minutes for deployment
3. You'll get a random URL like: `https://random-name-12345.netlify.app`

### Step 22: Change Site Name (Optional)

1. Go to **"Site settings"**
2. Click **"Change site name"**
3. Enter: `medadhere` (if available)
4. Your new URL: `https://medadhere.netlify.app`

---

## 🔒 Part 8: Update Azure CORS with Netlify URL

### Step 23: Update CORS in Azure

1. Go back to Azure Portal → Your Web App
2. Go to **"API"** → **"CORS"**
3. **Remove** the `*` wildcard
4. **Add** your Netlify URL:
   - `https://medadhere.netlify.app`
   - `https://www.medadhere.netlify.app` (if using custom domain)
5. Click **"Save"**

---

## ✅ Final Verification

### Step 24: Test Complete Application

1. **Open Netlify Site**: `https://medadhere.netlify.app`
2. **Test Features**:
   - ✅ Dashboard loads data
   - ✅ Pill Database search works
   - ✅ Identify Pill works
   - ✅ Add to Schedule works
   - ✅ Refresh button updates data

### Step 25: Check Browser Console

1. Press `F12` to open DevTools
2. Go to **Console** tab
3. Look for:
   ```
   🔧 API Configuration: {environment: 'Production', baseURL: 'https://medadhere-backend.azurewebsites.net'}
   ```

---

## 🎯 Your Deployed URLs

### Backend (Azure)
- **API**: https://medadhere-backend.azurewebsites.net
- **Docs**: https://medadhere-backend.azurewebsites.net/docs
- **Health**: https://medadhere-backend.azurewebsites.net/health

### Frontend (Netlify)
- **App**: https://medadhere.netlify.app (or your custom name)
- **Dashboard**: https://medadhere.netlify.app (default view)

---

## 🔧 Troubleshooting Common Issues

### Issue 1: Backend Shows "Application Error"

**Solution:**
1. Go to Azure Portal → Your Web App
2. Go to **"Monitoring"** → **"Log stream"**
3. Check for errors in logs
4. Common fixes:
   - Verify startup command is correct
   - Check `requirements.txt` has all dependencies
   - Ensure `gunicorn` is in requirements.txt

### Issue 2: Frontend Can't Connect to Backend

**Solution:**
1. Open browser DevTools (F12)
2. Check **Network** tab for failed requests
3. Verify:
   - Backend URL is correct in `config.js`
   - CORS is configured in Azure
   - Backend is actually running (test `/health` endpoint)

### Issue 3: GitHub Actions Deployment Fails

**Solution:**
1. Go to GitHub → Your Repository
2. Click **"Actions"** tab
3. Click on the failed workflow
4. Check error logs
5. Common fixes:
   - Verify `requirements.txt` exists in root
   - Check Python version matches (3.11)
   - Ensure no syntax errors in code

### Issue 4: Netlify Build Fails

**Solution:**
1. Check Netlify build logs
2. Ensure:
   - Base directory is `frontend`
   - No build command needed (or empty)
   - `frontend/index.html` exists

---

## 📊 Monitoring & Maintenance

### View Azure Metrics

1. Azure Portal → Your Web App
2. Go to **"Monitoring"** → **"Metrics"**
3. Track:
   - HTTP requests
   - Response time
   - CPU usage
   - Memory usage

### View Netlify Analytics

1. Netlify Dashboard → Your Site
2. Go to **"Analytics"** tab (may require paid plan)
3. Track:
   - Page views
   - Unique visitors
   - Bandwidth usage

---

## 💰 Cost Summary

### Azure App Service B1
- **Monthly**: ~$13
- **Features**: 1.75 GB RAM, 100 GB storage, custom domain, SSL

### Azure App Service F1 (Free Tier)
- **Monthly**: FREE
- **Limitations**: 60 minutes/day compute time, 1 GB storage

### Netlify
- **Monthly**: FREE
- **Limitations**: 100 GB bandwidth, 300 build minutes
- **Features**: Automatic SSL, CDN, custom domain

---

## 🎉 Congratulations!

Your MedAdhere application is now fully deployed!

- ✅ Backend running on Azure
- ✅ Frontend hosting on Netlify
- ✅ Automatic deployments via GitHub
- ✅ SSL certificates enabled
- ✅ CORS configured
- ✅ Environment auto-detection

---

## 📝 Next Steps (Optional)

1. **Custom Domain**: Add your own domain name
2. **CI/CD**: GitHub Actions is already set up!
3. **Monitoring**: Set up Azure Application Insights
4. **Database**: Migrate from JSON files to Azure PostgreSQL
5. **Storage**: Use Azure Blob Storage for images
6. **Authentication**: Add user authentication with Azure AD B2C

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review Azure Log Stream
3. Check Netlify deploy logs
4. Review GitHub Actions workflow logs

Happy deploying! 🚀
